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

"""Tests for get_commands"""

import unittest

from ots.server.allocator.get_commands import get_commands
from StringIO import StringIO

class TestGetCommands(unittest.TestCase):
    """Tests for get_commands"""

    def test_device_tests_with_packages(self):
        """Check conductor command with test packages for device"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "30"
        rootstrap = ""

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '30']
        
        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout)
        
        self.assertEquals(cmds[0].command, expected_cmds)

    def test_device_tests_with_packages_using_libssh2(self):
        """Check conductor command with test packages for device and libssh2"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz"}
        testrun_id = ""
        storage_address = ""
        test_filter = "-testsuite=testrunner-tests"
        timeout = "30"
        rootstrap = ""

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '30', '--libssh2']
        
        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout,
                            use_libssh2=True)
        
        self.assertEquals(cmds[0].command, expected_cmds)

    def test_device_tests_with_packages_using_resume(self):
        """Check conductor command with test packages for device and resume
        functionality"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz"}
        testrun_id = ""
        storage_address = ""
        test_filter = "-testsuite=testrunner-tests"
        timeout = "30"
        rootstrap = ""

        expected_cmds = ['conductor',
                         '-u', 'http://image/url/image.bin',
                         '-f', '-testsuite=testrunner-tests',
                         '-t', "foo,bar,baz", '-m', '30', '--resume']
        
        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout,
                            resume=True)
        
        self.assertEquals(cmds[0].command, expected_cmds)

    def test_custom_distribution_models(self):
        """Check that custom distribution models can be used"""
        self.model_called = 0

        def custom_model1(test_list, options):
            self.model_called = 1
            return ["asdf"]

        distribution_model = "custom1"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"
        timeout = "60"
        rootstrap = ""

        expected_cmds = ["asdf"]
        
        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout,
                            custom_distribution_model = custom_model1)

        self.assertEquals(cmds, expected_cmds)


    def test_device_tests_with_no_packages(self):
        """Check conductor command without test packages for device"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "20"
        rootstrap = ""

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests', '-m', '20']
        
        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout)
        
        self.assertEquals(cmds[0].command, expected_cmds)


    def test_host_tests(self):
        """Check conductor command with test packages for host"""

        expected_cmds = ['conductor',
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '20',
                          '-o']


        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'host':"foo,bar,baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"
        timeout = "20"
        rootstrap = ""

        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout)
        
        self.assertEquals(cmds[0].command, expected_cmds)

    def test_chroot_tests(self):
        """Check conductor command with test packages for chroot"""

        expected_cmds = ['conductor',
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '20',
                          '--chrooted', "--rootstrapurl=url_to_rootstrap"]

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'chroot':"foo,bar,baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"
        timeout = "20"
        rootstrap = "url_to_rootstrap"

        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout)

        self.assertEquals(cmds[0].command, expected_cmds)

    def test_device_and_host_tests_no_flasher(self):
        """Check conductor command with packages for device and host, without flasherurl."""

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin',
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '20',
                          ';',
                          'conductor',
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '-t', "foo,bar,baz", '-m', '20',
                          '-o']


        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz",'host':"foo,bar,baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "20"
        rootstrap = ""

        cmds = get_commands(distribution_model,
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout)
        
        self.assertEquals(cmds[0].command, expected_cmds)

        

    def test_device_and_host_tests_with_flasher(self):
        """
        Check conductor command with packages for device and host,
        with flasher URL.
        """

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin',
                          '-f', '-testsuite=testrunner-tests',
                          '--flasherurl', "asdfasdf/asdf",
                          '-t', "foo,bar,baz", '-m', '60',
                          ';',
                          'conductor',
                          '-u', 'http://image/url/image.bin', 
                          '-f', '-testsuite=testrunner-tests',
                          '--flasherurl', "asdfasdf/asdf",
                          '-t', "foo,bar,baz", '-m', '60',
                          '-o']


        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar,baz",'host':"foo,bar,baz"}
        testrun_id = ""
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"
        timeout = "60"
        flasher = "asdfasdf/asdf"
        rootstrap = ""

        cmds = get_commands(distribution_model, 
                            image_url,
                            rootstrap,
                            test_list,
                            testrun_id,
                            storage_address,
                            test_filter,
                            timeout,
                            flasher)
        
        self.assertEquals(cmds[0].command, expected_cmds)



    def test_device_tests_with_packages_in_distribution_perpackage(self):
        """Test distribution perpackage - device_tests_with_packages"""

        expected_cmd_1 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "foo", '-m', '30']
        expected_cmd_2 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "bar", '-m', '30']

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "30"
        rootstrap = ""

        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)


    def test_device_tests_with_one_pkg_in_distribution_perpackage(self):
        """Test distribution perpackage - device_tests_with_packages"""

        expected_cmd_1 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "foo", '-m', '30']

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "30"
        rootstrap = ""

        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        self.assertEquals(len(commands), 1)
        self.assertEquals(commands[0].command, expected_cmd_1)


    def test_host_tests_with_packages_in_distribution_perpackage(self):
        """Test distribution perpackage - host_tests"""

        expected_cmd_1 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "foo", '-m', '30',
                        '-o']
        expected_cmd_2 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "bar", '-m', '30',
                        '-o']

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_list = {'host':"foo,bar"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "30"
        rootstrap = ""

        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)
        
        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)


    def test_device_and_host_tests_in_distribution_perpackage(self):
        """Test distribution perpackage - device_and_host_tests"""

        expected_cmd_1 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "foo", '-m', '10']
        expected_cmd_2 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "bar", '-m', '10']
        expected_cmd_3 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "baz", '-m', '10',
                        '-o']
        expected_cmd_4 = ['conductor', 
                        '-u', 'http://image/url/image.bin', 
                        '-f', '-testsuite=testrunner-tests',
                        '-t', "yaz", '-m', '10',
                        '-o']

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_list = {'device':"foo,bar",'host':"baz,yaz"}
        testrun_id = "" 
        storage_address = ""
        timeout = "10"
        test_filter = "-testsuite=testrunner-tests"
        rootstrap = ""
        
        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        self.assertEquals(len(commands), 4)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        self.assertEquals(commands[2].command, expected_cmd_3)
        self.assertEquals(commands[3].command, expected_cmd_4)


    def test_device_tests_with_no_packages_in_distribution_perpackage(self):
        """Test distribution perpackage - no packages"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_list = {} #no packages
        testrun_id = "" 
        storage_address = "" 
        test_filter = "-testsuite=testrunner-tests"  
        timeout = "30"
        rootstrap = ""

        self.assertRaises(ValueError,
                          get_commands,
                          distribution_model,
                          image_url,
                          rootstrap,
                          test_list,
                          testrun_id,
                          storage_address,
                          test_filter,
                          timeout)

    def test_device_tests_with_one_testplan(self):
        """Test device test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_list = {'hw_testplans': [test_plan]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml']


        self.assertEquals(len(commands), 1)
        self.assertEquals(commands[0].command, expected_cmds)

    def test_device_tests_with_multiple_testplans(self):
        """Test device test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'hw_testplans': [test_plan, test_plan2]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml']
        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml']


        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        
    def test_host_tests_with_one_testplan(self):
        """Test host test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_list = {'host_testplans': [test_plan]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']


        self.assertEquals(len(commands), 1)
        self.assertEquals(commands[0].command, expected_cmds)

    def test_host_tests_with_multiple_testplans(self):
        """Test host test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'host_testplans': [test_plan, test_plan2]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']
        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml', '-o']


        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        
    def test_mixed_tests_with_multiple_testplans(self):
        """Test host test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'host_testplans': [test_plan], 'hw_testplans' : [test_plan2]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml']
        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']


        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        
    def test_mixed_tests_with_multiple_testplans_and_pkgs(self):
        """Test host test plan based - one test plan"""

        distribution_model = "default"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'host_testplans': [test_plan], 'hw_testplans' : [test_plan2],
                     'device':"foo,bar",'host':"baz,yaz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin',
                          '-t', "foo,bar", '-m', '30',
                          ';',
                          'conductor',
                          '-u', 'http://image/url/image.bin',
                          '-t', "baz,yaz", '-m', '30',
                          '-o']

        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml']
        expected_cmd_3 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']


        self.assertEquals(len(commands), 3)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        self.assertEquals(commands[2].command, expected_cmd_3)


    def test_device_tests_with_one_testplan_perpackage(self):
        """Test device test plan based - one test plan"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_list = {'hw_testplans': [test_plan]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml']


        self.assertEquals(len(commands), 1)
        self.assertEquals(commands[0].command, expected_cmds)

    def test_device_tests_with_multiple_testplans_perpackage(self):
        """Test device test plan based - one test plan"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'hw_testplans': [test_plan, test_plan2]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml']
        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml']


        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        
    def test_host_tests_with_one_testplan_perpackage(self):
        """Test host test plan based - one test plan"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_list = {'host_testplans': [test_plan]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url, 
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmds = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']


        self.assertEquals(len(commands), 1)
        self.assertEquals(commands[0].command, expected_cmds)

    def test_host_tests_with_multiple_testplans_perpackage(self):
        """Test host test plan based - one test plan"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'host_testplans': [test_plan, test_plan2]}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']
        expected_cmd_2 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml', '-o']


        self.assertEquals(len(commands), 2)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)

    def test_mixed_tests_with_multiple_testplans_and_pkgs_perpackage(self):
        """Test host test plan based - one test plan"""

        distribution_model = "perpackage"
        image_url = 'http://image/url/image.bin'
        test_plan = StringIO("hulapaloo")
        test_plan.name = "testplan.xml"
        test_plan2 = StringIO("hulapaloo2")
        test_plan2.name = "testplan2.xml"
        test_list = {'host_testplans': [test_plan], 'hw_testplans' : [test_plan2],
                     'device':"foo",'host':"baz"}
        testrun_id = "" 
        storage_address = "" 
        test_filter = ""  
        timeout = "30"
        rootstrap = ""
        commands = get_commands(distribution_model, 
                                image_url,
                                rootstrap,
                                test_list,
                                testrun_id,
                                storage_address,
                                test_filter,
                                timeout)

        expected_cmd_1 = ['conductor', 
                          '-u', 'http://image/url/image.bin',
                          '-t', "foo", '-m', '30',
                          ]
        expected_cmd_2 = [
                          'conductor',
                          '-u', 'http://image/url/image.bin',
                          '-t', "baz", '-m', '30',
                          '-o']

        expected_cmd_3 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan2.xml']
        expected_cmd_4 = ['conductor', 
                          '-u', 'http://image/url/image.bin', 
                          '-m', '30', '-p', 'testplan.xml', '-o']

        self.assertEquals(len(commands), 4)
        self.assertEquals(commands[0].command, expected_cmd_1)
        self.assertEquals(commands[1].command, expected_cmd_2)
        self.assertEquals(commands[2].command, expected_cmd_3)
        self.assertEquals(commands[3].command, expected_cmd_4)




#######################################################################


if __name__ == "__main__":
    unittest.main()
