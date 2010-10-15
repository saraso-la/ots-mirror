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
Very much a spike
"""

import sys
import os
import logging
import logging.config
import uuid
import ConfigParser
from socket import gethostname

from ots.common.framework.api import config_filename

from ots.server.distributor.api import taskrunner_factory

from ots.server.hub.testrun import testrun
from ots.server.hub.options_factory import options_factory
from ots.server.hub.plugins import ReportPlugin
from ots.server.hub.plugins import BifhPlugin
from ots.server.hub.conductor_command import get_commands
from ots.server.hub.application_id import get_application_id


LOG = logging.getLogger(__name__)

#FIXME: Hackish implementation WIP whilst DataStoring in development 
from ots.report_plugin.tests.test_report_plugin import DataStoringStub 
DATA_STORING_STUB = DataStoringStub()


def _init_logging():
    """
    Initialise the logging from the configuration file
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    conf = os.path.join(dirname, "logging.conf")
    logging.config.fileConfig(conf)


########################
# Configuration stuff
########################

def _timeout():
    """
    rtype: C{int}
    rparam: The timeout in minutes
    """
    server_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    app_id = get_application_id() 
    conf = config_filename(app_id, server_path)
    config = ConfigParser.ConfigParser()
    config.read(conf)       
    return int(config.get('ots.server.hub', 'timeout'))

def _storage_address():
    """
    rtype: C{str}
    rparam: The storage address 
    """
    server_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    app_id = get_application_id() 
    conf = config_filename(app_id, server_path)
    config = ConfigParser.ConfigParser()
    config.read(conf)
    storage_host = str(config.get('ots.server.hub', 'storage_host'))
    if not storage_host:
        storage_host = gethostname()
    storage_port = str(config.get('ots.server.hub', 'storage_port'))  
    return "%s:%s"%(storage_host, storage_port)     

#####################

def _primed_taskrunner(testrun_uuid, timeout, storage_address, options): 
    """
    Get a Taskrunner loaded with Tasks and ready to Run

    type testrun_uuid:
    param testrun_uuid:

    type timeout:
    param timeout:

    type storage_address:
    param storage_address: 

    type options: 
    param options:

    rtype: C{str}
    rparam: The storage address 
    """
    taskrunner = taskrunner_factory(options.device, timeout, testrun_uuid)
 
    #Is this the API for kickstart?
    cmds = get_commands(options.is_package_distributed,
                        options.image_url,
                        options.hw_packages,
                        options_host_packages,
                        options.emmc,
                        options.testrun_uuid,
                        storage_address,
                        options.testfilter,
                        options.flasher)
    for cmd in cmds:
        taskrunner.add_task(cmd)
    return taskrunner



def run(sw_product, request_id, notify_list, **kwargs):
    #FIXME the epydoc for the new api once stabilised
    sw_product = sw_product.lower()
    
    options = options_factory(sw_product, kwargs)
    taskrunner = _primed_taskrunner(testrun_uuid, 
                                    _timeout(),
                                    _storage_address(),
                                    options)
    run(sw_product, request_id, notify_list, taskrunner.run, options)

def _run(sw_product, request_id, testrun_uuid, 
        notify_list, run_test, options):

    #FIXME the epydoc for the new api once stabilised
    """
    @type sw_product: C{string}
    @param sw_product: Name of the sw product this testrun belongs to

    @type request_id: C{string}
    @param request_id: An identifier for the request from the client

    @param notify_list: Email addresses for notifications
    @type product: C{list}
    """
    bifh_plugin = BifhPlugin(request_id)
    target_packages = []
    if bifh_plugin is not None:
        target_packages = bifh_plugin.get_target_packages(request_id)


    #FIXME: Hackish initialisation as Datastoring is a WIP

    #TODO add testrun_id mapping

    report_plugin = ReportPlugin(DATA_STORING_STUB,
                                 request_id,
                                 options.testplan_id,
                                 sw_product,
                                 options.gate,
                                 options.label,
                                 options.hw_packages,
                                 options.image,
                                 target_packages)

    _init_logging()
    #Preprocessing_steps_here?

    try:
        LOG.debug("Initialising Testrun")
        is_hw_enabled = bool(len(options.hw_packages))
        is_host_enabled = bool(len(options.host_packages))
        result = testrun(run_test, 
                         is_hw_enabled = is_hw_enabled, 
                         is_host_enabled = is_host_enabled)
        LOG.debug("Testrun finished with result: %s"%(result))
        if report_plugin is not None:
            report_plugin.result = result
    except Exception, err:
        LOG.debug("Testrun Exception: %s"%(err))
        import traceback
        LOG.debug(traceback.format_exc())
        if report_plugin is not None:
            report_plugin.exception = sys.exc_info()[1]


    #Some post_processing steps here?
