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
The Hub provides a focal point for inter-component data-flow in the
OTS system.

Hence OTS suggests a centralised topology 
with the Hub as it's central component.

The role of the Hub is the high level management of a single Testrun.

Specifically:

 - Receive test request from third-party client
 - Allocate Tasks 
 - Dispatch Testrun
 - Receives results
 - Publish results

"""

import sys
import os
import logging
import logging.config
import uuid
import ConfigParser
import traceback

from ots.common.framework.api import config_filename

from ots.server.allocator.api import primed_taskrunner

from ots.server.hub.testrun import Testrun
from ots.server.hub.options_factory import OptionsFactory
from ots.server.hub.application_id import get_application_id
from ots.server.hub.publishers import Publishers

LOG = logging.getLogger(__name__)

class Hub(object):

    """
    The Hub is the Keystone of the OTS system
    """

    def __init__(self, sw_product, request_id, **kwargs):
        """
        @type sw_product: C{str}
        @param sw_product: Name of the sw product this testrun belongs to

        @type request_id: C{str}
        @param request_id: An identifier for the request from the client
        """
        self.sw_product = sw_product.lower()
        self.request_id = request_id
        options_factory = OptionsFactory(sw_product, kwargs)
        options = options_factory()
        self.testrun_uuid = uuid.uuid1().hex 
        self.publishers = Publishers(request_id, 
                                     testrun_uuid, 
                                     sw_product, 
                                     options.image,
                                     options_factory.extended_options_dict)

    #########################
    # HELPERS
    #########################

    @staticmethod
    def _init_logging():
        """
        Initialise the logging from the configuration file
        """
        #FIXME
        dirname = os.path.dirname(os.path.abspath(__file__))
        conf = os.path.join(dirname, "logging.conf")
        logging.config.fileConfig(conf)

    @property
    def _timeout(self):
        """
        rtype: C{int}
        rparam: The timeout in minutes
        """
        server_path = os.path.split(
            os.path.dirname(os.path.abspath(__file__)))[0]
        app_id = get_application_id() 
        conf = config_filename(app_id, server_path)
        config = ConfigParser.ConfigParser()
        config.read(conf)       
        return int(config.get('ots.server.hub', 'timeout'))

    ###############################
    # TASKRUNNER
    ##############################

    @property 
    def taskrunner(self):
        """
        A Taskrunner loaded with Tasks as 
        allocated by preferences

        rtype : L{ots.server.distributor.taskrunner}
        rparam : A Taskrunner loaded with Tasks
        """
        taskrunner = primed_taskrunner(testrun_uuid, 
                                       self._timeout,
                                       self.options.priority,
                                       self.options.device,
                                       self.options.image,
                                       self.options.hw_packages,
                                       self.options.host_packages,
                                       self.options.emmc,
                                       self.options.testfilter,
                                       self.options.flasher,
                                       self.publishers)

        return taskrunner

    ################################
    # RUN
    ################################

    def run(self):
        """
        Start a Testrun and publish the data 
        """    

        LOG.debug("Initialising Testrun")
        try:
            is_hw_enabled = bool(len(options.hw_packages))
            is_host_enabled = bool(len(options.host_packages))
            testrun = Testrun(is_hw_enabled = is_hw_enabled, 
                              is_host_enabled = is_host_enabled)
            testrun.run_test = run_test
            testrun_result = testrun.run()
            LOG.debug("Testrun finished with result: %s"%(testrun_result))

            self.publishers.set_testrun_result(testrun_result)
            self.publishers.set_expected_packages(testrun.expected_packages)
            self.publishers.set_tested_packages(testrun.tested_packages)
            self.publishers.set_results(testrun.results)
            self.publishers.set_monitors(testrun.monitors)

        except Exception, err:
            LOG.debug("Testrun Exception: %s"%(err))
            LOG.debug(traceback.format_exc())
            self.publishers.set_exception(sys.exc_info()[1])

        self.publishers.publish() 
