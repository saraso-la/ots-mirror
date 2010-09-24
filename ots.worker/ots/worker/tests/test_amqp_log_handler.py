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

import unittest 

import logging
import logging.handlers

from amqplib import client_0_8 as amqp

from ots.common.amqp.api import unpack_message
from ots.worker.amqp_log_handler import AMQPLogHandler

def _init_queue(channel, queue, exchange, routing_key):
    """
    Initialise a durable queue and a direct exchange
    with a routing_key of the name of the queue

    @type channel: C{amqplib.client_0_8.channel.Channel}  
    @param channel: The AMQP channel

    @rtype queue: C{string}  
    @return queue: The queue name
    """
    channel.queue_declare(queue = queue, 
                          durable = False, 
                          exclusive = False,
                          auto_delete=True)
    channel.exchange_declare(exchange = exchange,
                             type = 'direct',
                             durable = False,
                             auto_delete = True)
    channel.queue_bind(queue = queue,
                       exchange = exchange,
                       routing_key = routing_key)


class TestAMQPLogHandler(unittest.TestCase):

    def test_on_message_not_version_compatible(self):
        """
        Check that incompatible versions dont
        pull messages from the queue
        """
        #Set up the AMQP Channel
        connection = amqp.Connection(host = "localhost", 
                                          userid = "guest",
                                          password = "guest",
                                          virtual_host = "/", 
                                          insist = False)
        channel = connection.channel()
        _init_queue(channel, 
                    "test", 
                    "test",
                    "test")

        #Initialise the Logger
        logging.basicConfig(filename = None,
                    level=logging.DEBUG)
        logger = logging.getLogger()
        logging.handlers.AMQPLogHandler = AMQPLogHandler

        #Initialise the Handler
        handler = AMQPLogHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        handler.channel = channel
        handler.exchange = "test"
        handler.queue = "test"

        #Log 
        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")

        #Consume
        records = []
        def cb(message):
            channel.basic_ack(delivery_tag = message.delivery_tag)
            records.append(unpack_message(message))
        channel.basic_consume("test", callback = cb)
        for i in range(4):
            channel.wait()
        
        #Validate
        messages = [rec.message for rec in records]
        self.assertEquals(['debug', 'info', 'warning', 'error'],
                          messages)
       
       

if __name__ == "__main__":
    unittest.main()
        
        
