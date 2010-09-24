# ***** BEGIN LICENCE BLOCK *****

# This file is part of OTS
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: Mikko Makinen <mikko.al.makinen@nokia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
# ***** END LICENCE BLOCK *****

"""
The Task Broker is the heart of the Worker.

Listen for messages containing Tasks 
from RabbitMQ and dispatch
the Tasks as (Blocking) Processes.

The simple implementation will hold as long as 
the following assumptions holding true:

1. There is only a single resource providing i/o (RabbitMQ)
2. Tasks are blocking
3. Tasks are run in Serial 
"""

#Disable spurious pylint warnings

#pylint: disable-msg=E0611
#pylint: disable-msg=F0401

import os
import sys
from time import sleep
import logging
from itertools import cycle

from ots.common.amqp.api import unpack_message, pack_message
from ots.common.dto.api import StateChangeMessage, TaskCondition

import ots.worker
from ots.worker.command import Command
from ots.worker.command import SoftTimeoutException,  HardTimeoutException
from ots.worker.command import CommandFailed

LOGGER = logging.getLogger(__name__)

STOP_SIGNAL_FILE = "/tmp/stop_ots_worker"

TASK_CONDITION_RESPONSES = [TaskCondition.START,
                            TaskCondition.FINISH]

class NotConnectedError(Exception):
    """Exception raised if not connected to amqp"""
    pass

########################################
# Command Class to Function
########################################

def _start_process(command, timeout):
    """
    Starts the specified process

    @type command: string
    @param command: The CL params for the Process to be run as a Task 

    @type timeout: int
    @param timeout: The timeout to apply to the Task
    """
    task = Command(command, 
                   soft_timeout=timeout,
                   hard_timeout=timeout + 5)

    task.execute()


##############################
# TASK_BROKER
##############################

class TaskBroker(object):
    """
    Listens to a Queue of the given Routing Key.
    Pulls messages containing Tasks from AMQP 
    Dispatch the Tasks as a process
    """   
    def __init__(self, connection, queue, routing_key, services_exchange):
        self._connection = connection
        self.queue = queue
        self.routing_key = routing_key
        self.services_exchange = services_exchange
        self._keep_looping = True
        self._consumer_tag = ""

        self._task_state = cycle(TASK_CONDITION_RESPONSES)
        self._amqp_log_handler = None

    ############################################
    # LOG HANDLER
    ############################################

    def _set_amqp_log_handler(self, amqp_log_handler)
        self._amqp_log_handler = amqp_log_handler
        self._amqp_log_handler.channel = self.channel

    amqp_log_handler = property(None, _set_amqp_log_handler)

    #############################################
    # AMQP CONNECTION PROPERTIES 
    #############################################

    @property 
    def channel(self):
        """amqp channel"""
        channel = self._connection.channel
        if channel is not None:
            return channel
        else:
            raise NotConnectedError()

    ##############################################
    # AMQP Configuration
    ##############################################
       
    def _consume(self):
        """
        Start consuming messages from the queue
        Ensures that only one message is taken at a time
        """
        self.channel.basic_qos(0, 1, False)
        self._consumer_tag = self.channel.basic_consume(queue = self.queue, 
                                                   callback = self._on_message)

    def _init_connection(self):
        """
        Initialise the connection to AMQP.
        Queue and Services Exchange are both durable
        """
        self.channel.queue_declare(queue = self.queue, 
                                   durable = True,
                                   exclusive = False, 
                                   auto_delete = False)
        self.channel.exchange_declare(exchange = self.services_exchange,
                                      type = 'direct', 
                                      durable = True,
                                      auto_delete = False)
        self.channel.queue_bind(queue = self.queue,
                                exchange = self.services_exchange,
                                routing_key = self.routing_key)

    ###############################################
    # LOOPING / HANDLING / DISPATCHING
    ###############################################

    def _cancel(self):
        self.channel.basic_cancel(self._consumer_tag)

    def _loop(self):
        """
        The main loop
        Continually listen for messages coming from RabbitMQ
        """
        LOGGER.debug("Starting main loop...")
        while self._keep_looping:
            try:
                if not self._stop_file_exists():
                    self.channel.wait()
                else:
                    self._keep_looping = False
            except Exception:
                #FIXME Check logs to see what exceptions are raised here
                LOGGER.exception("_loop() failed")
                self._try_reconnect()
        self._clean_up()

    def _handle_message(self, message):
        """
        The Message Handler. 
        
        @type message: amqplib.client_0_8.basic_message.Message 
        @param message: A message containing a pickled dictionary

        This turns off the connection on receipt of a message.
        Once the Task has run the connection is reestablished.

        Response Queue is kept informed of the status
        """
        
        self.channel.basic_cancel(self._consumer_tag)
        self.channel.basic_ack(delivery_tag = message.delivery_tag)
        #
        cmd_msg = unpack_message(message)
        task_id = cmd_msg.task_id
        response_queue = cmd_msg.response_queue
        #
        if self._amqp_log_handler is not None:
            self._amqp_log_handler.queue = response_queue
            self._amqp_log_handler.exchange = response_queue
        #
        self._publish_task_state_change(task_id, response_queue)
        #
        try:
            self._dispatch(cmd_msg)
        except (HardTimeoutException, 
                SoftTimeoutException,
                CommandFailed):
            exception = sys.exc_info()[1]
            exception.task_id = task_id 
            self._publish_exception(response_queue,
                                    exception)
        finally:
            self._publish_task_state_change(task_id, response_queue)
            LOGGER.info("Recommence consume on queue: %s" % self.queue)
            self._consumer_tag = \
                self.channel.basic_consume(queue = self.queue,
                                           callback = self._on_message)

    def _on_message(self, message):
        """
        The High Level Message Handler. 
        Handles messages if the Worker is version compatible 
        
        @type message: amqplib.client_0_8.basic_message.Message 
        @param message: A message containing a pickled dictionary
        """
        LOGGER.debug("Received Message")
        if self._is_version_compatible(message):
            self._handle_message(message)
        else:
            LOGGER.debug("Worker not version compatible")
            #Close the connection makes message available to other Workers
            self._clean_up()

    def _dispatch(self, cmd_msg):
        """
        Dispatch the Task. Currently as a Process (Blocking)
                
        @type message: C{ots.common.amqp.messages.CommandMessage
        @param message: The CL params for the Process to be run as a Task 
        """

        if cmd_msg.is_quit:
            self._keep_looping = False
        elif not cmd_msg.is_ignore:
            LOGGER.debug("Running command: '%s'"%(cmd_msg.command))
            _start_process(command = cmd_msg.command, 
                           timeout = cmd_msg.timeout)
            
    ########################################
    # MESSAGE PUBLISHING
    ########################################

    def _publish_task_state_change(self, task_id, response_queue):

        """
        Inform the response queue of the status of the Task

        @type response_queue: string
        @param response_queue: The name of the response queue 
        """
        state = self._task_state.next()
        LOGGER.debug("Task in state: '%s'"%(state))
        state_msg = StateChangeMessage(task_id, state)
        amqp_message = pack_message(state_msg) 
        self.channel.basic_publish(amqp_message,
                                   mandatory = True,
                                   exchange = response_queue,
                                   routing_key = response_queue)


    def _publish_exception(self, response_queue, exception):
        """
        Put an Exception on the response queue 

        @type response_queue: C{str}
        @param response_queue: The name of the response queue 

        @type exception: L{OTSException}
        @param exception: An OTSException 

        """
        message = pack_message(exception)
        self.channel.basic_publish(message,
                                   mandatory = True,
                                   exchange = response_queue,
                                   routing_key = response_queue)

    #######################################
    # HELPERS
    #######################################

    def _is_version_compatible(self, message):
        """
        Is the Worker version compatible

        @type message: amqplib.client_0_8.basic_message.Message 
        @param message: A message containing a pickled dictionary

        @rtype: C{bool}
        @rparam: Returns True if compatible otherwise false
        """
        ret_val = True
        cmd_msg = unpack_message(message)
        min_worker_version = cmd_msg.min_worker_version

        if min_worker_version is not None:
            major_minor, revision = ots.worker.__VERSION__.split("r")
            LOGGER.debug("Min version: %s. Worker version: %s"%
                         (min_worker_version, major_minor))
            ret_val = float(major_minor) >= float(min_worker_version)
        return ret_val
        
    def _try_reconnect(self):
        """
        A poorly implemented reconnect to AMQP
        """
        #FIXME: Move out into own connection module.
        #Implement with a exponential backoff with max retries.
        LOGGER.exception("Error. Waiting 5s then retrying")
        sleep(5)
        try:
            LOGGER.info("Trying to reconnect...")
            self._connection.connect()
            self._init_connection()
            self._consume()
        except Exception:
            #If rabbit is still down, we expect this to fail
            LOGGER.exception("Reconnecting failed...")

    def _clean_up(self):
        """
        Delegate to connection cleanup
        """
        try:
            self.channel.basic_cancel(self._consumer_tag)
        except:
            pass
        if self._connection:
            self._connection.clean_up()

    def __del__(self):
        """
        Destructor
        """
        self._clean_up()

    @staticmethod
    def _stop_file_exists():
        """
        Check whether the stop file is in place
        
        @rtype stop: C{bool} 
        @return stop: Is stop file present
        """
        stop = False
        if os.path.exists(STOP_SIGNAL_FILE):
            os.system("rm -fr "+STOP_SIGNAL_FILE)
            LOGGER.info("Worker was asked to stop after testrun ready.")
            stop = True
        return stop
      
    ################################
    # PUBLIC METHODS
    ################################
        
    def run(self):
        """ 
        Polls RabbitMQ for Task Messages and runs the Tasks.

        Initialises the AMQP connections and run the forever loop.
        """
        self._init_connection()
        self._consume()
        self._loop()
