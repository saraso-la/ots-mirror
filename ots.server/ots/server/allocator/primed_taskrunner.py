# ***** BEGIN LICENCE BLOCK *****
# This file is part of OTS
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: meego-qa@lists.meego.com
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

""" Creates tasks for taskrunner """

import logging
from socket import gethostname
import configobj

from ots.common.routing.api import get_routing_key

from ots.server.server_config_filename import server_config_filename
from ots.server.distributor.api import taskrunner_factory
from ots.server.allocator.get_commands import get_commands

LOG = logging.getLogger(__name__)

class AllocatorException(Exception):
    """AllocatorExceptionNoCommands"""
    pass

def _storage_address():
    """
    rtype: C{str}
    rparam: The storage address 
    """
    
    conf = server_config_filename()
    config = configobj.ConfigObj(conf).get('ots.server.allocator')
    storage_host = config['storage_host']
    if not storage_host:
        storage_host = gethostname()

    # TODO: DEPRECATED REMOVE AFTER CONDUCTOR IS CHANGED
    storage_port = "1982" 
    return "%s:%s" % (storage_host, storage_port)     



#####################
# PUBLIC METHOD
#####################


def primed_taskrunner(testrun_uuid, execution_timeout, distribution_model, 
                      device_properties, image, rootstrap, hw_packages,
                      host_packages, chroot_packages, hw_testplans,
                      host_testplans, emmc, testfilter, flasher, use_libssh2,
                      resume, custom_distribution_model, flasher_options,
                      extended_options): 

    """
    Get a Taskrunner loaded with Tasks and ready to Run

    @type testrun_uuid: C{str}
    @param testrun_uuid: The unique identifier for the testrun

    @type execution_timeout: C{int}
    @param execution_timeout: The execution timeout in minutes

    @type distribution_model: C{str}
    @param distribution_model: The name of the distribution_model

    @type device_properties : C{dict}
    @param device_properties : A dictionary of device properties 
                               this testrun requires

    @type image: C{str}
    @param image: The URL of the image

    @type rootstrap : C{str}
    @param rootstrap: Url to the chroot rootstrap

    @type hw_packages : C{list} of C{str}
    @param hw_packages: The hardware packages

    @type host_packages : C{list} of C{str}
    @param host_packages: The host packages
    
    @type hw_testplans : C{list} of C{str}
    @param hw_testplans: The hardware test plans

    @type host_testplans : C{list} of C{str}
    @param host_testplans: The host test plans

    @type emmc : C{str}
    @param emmc: Url to the additional content image (memory card image)
      
    @type testfilter: C{str}
    @param testfilter: The test filter string for testrunner-lite

    @type flasher: C{str}
    @param flasher: The URL of the flasher

    @type use_libssh2: C{boolean}
    @param use_libssh2: Use testrunner-lite libssh2 support

    @type resume:  C{boolean}
    @param resume: Use testrunner-lite resume functionality

    @type custom_distribution_model: C{callable}
    @param custom_distribution_model: A callable matching the default models
                                      in default_distribution_models.py

    @type flasher_options : C{string}
    @param flasher_options : Custom flasher options

    @type extended_options : C{dict}
    @param extended_options : A dictionary of extended ots testrun options

    @rtype: C{Taskrunner}
    @return: A loaded Taskrunner 
    """

    routing_key = get_routing_key(device_properties)
    taskrunner = taskrunner_factory(routing_key, execution_timeout, 
                                    testrun_uuid)
    test_list = dict()

    if hw_packages:
        test_list['device'] = ",".join(hw_packages)
    if host_packages:
        test_list['host'] = ",".join(host_packages)

    if hw_testplans:
        test_list['hw_testplans'] = hw_testplans
    if host_testplans:
        test_list['host_testplans'] = host_testplans

    if chroot_packages:
        test_list['chroot'] = ",".join(chroot_packages)

    # Server deals with minutes, conductor uses seconds, 
    execution_timeout = int(execution_timeout)*60

    cmds = get_commands(distribution_model,
                        image,
                        rootstrap,
                        test_list,
                        testrun_uuid,
                        _storage_address(),
                        testfilter,
                        execution_timeout,
                        flasher,
                        custom_distribution_model,
                        use_libssh2,
                        resume,
                        flasher_options,
                        extended_options)
    
    if len(cmds) == 0:
        raise AllocatorException("No commands created!")


    for cmd in cmds:
        LOG.info("Added cmd '%s' to taskrunner" % (" ".join(cmd.command)))
        taskrunner.add_task(cmd)
    return taskrunner
