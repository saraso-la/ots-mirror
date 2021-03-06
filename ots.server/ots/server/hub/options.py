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

"""
Defines the interface for the
Testrun options
as provided by OTS clients.
"""

from ots.server.hub.parameters_parser import string_2_list, string_2_dict
from StringIO import StringIO
from copy import deepcopy

############################
# FLAGS
############################

TRUE = "true"
FALSE = "false"
ON = "on"

#################################
# PACKAGE NAMING DEFINITIONS
#################################

TESTS = "-tests"
TEST = "-test"
BENCHMARK = "-benchmark"

VALID_PKG_SUFFIXES = [TESTS, TEST, BENCHMARK]

###################################
# Options
###################################


class Options(object):
    """
    Interface for the options available to the client
    """

    def __init__(self, image, rootstrap=None, packages=None, plan=None,
                 hosttest=None, chroottest=None, device=None, emmc=None,
                 distribution_model=None, flasher=None, testfilter=None,
                 hw_testplans=None, host_testplans=None, timeout=None,
                 use_libssh2=None, resume=None, flasher_options=None):

        """
        @type image: C{image}
        @param image: The image URL

        @type rootstrap: C{str}
        @param rootstrap: The rootstrap URL

        @type packages: C{str}
        @param packages: Test packages

        @type plan: C{str}
        @param plan: Test plan id

        @type hosttest: C{str}
        @param hosttest: Host test cases

        @type chroottest: C{str}
        @param chroottest: Chroot test cases

        @type device: C{dict}
        @param device: Device properties

        @type emmc: C{str}
        @param emmc: Url to the additional content image

        @type distribution_model: C{str}
        @param distribution_model: The name of ditribution model

        @type flasher: C{str}
        @param flasher: URL of the flasher

        @type testfilter: C{str}
        @param testfilter: The test filter string for testrunner-lite

        @type timeout: C{str}
        @param timeout: Test execution timeout in minutes

        @type use_libssh2: C{boolean}
        @param use_libssh2: Use testrunner-lite libssh2 support

        @type resume: C{boolean}
        @param resume: Use testrunner-lite resume functionality

        @type flasher_options: C{string}
        @param flasher_options: Custom options for flasher

        """
        self._image = image
        if not packages:
            packages = []
        self._packages = packages
        self._plan = plan
        if not hosttest:
            hosttest = []
        if not hw_testplans:
            hw_testplans = []
        self._hw_testplans = hw_testplans
        if not host_testplans:
            host_testplans = []
        self._host_testplans = host_testplans
        self._hosttest = hosttest
        if not device:
            device = dict()
        if not chroottest:
            chroottest = []
        self._chroottest = chroottest
        self._rootstrap = rootstrap
        self._device = device
        self._emmc = emmc
        self._distribution_model = distribution_model
        self._flasher = flasher
        self._testfilter = testfilter
        self._use_libssh2 = use_libssh2
        self._resume = resume
        self._timeout = timeout
        self._flasher_options = flasher_options

        self._validate_packages(self.hw_packages)
        self._validate_packages(self.host_packages)
        self._validate_packages(self.chroot_packages)
        self._validate_distribution_models(distribution_model,
                                           self.hw_packages \
                                               + self.host_packages \
                                               + self.hw_testplans \
                                               + self.host_testplans \
                                               + self.chroot_packages)
        self._validate_chroot(self._rootstrap, self.chroot_packages)

    ##################################
    # PROPERTIES
    ##################################

    @property
    def image(self):
        """
        The URL of the image
        @rtype: C{str}
        """
        return self._image

    @property
    def rootstrap(self):
        """
        The URL of the chroot rootstrap file
        @rtype: C{str}
        """
        return self._rootstrap

    @property
    def hw_packages(self):
        """
        Packages for hardware testing
        @rtype: C{list} of C{str}
        """
        return string_2_list(self._packages)

    @property
    def host_packages(self):
        """
        Packages for host testing
        @rtype: C{list} of C{str}
        """
        return string_2_list(self._hosttest)
    
    @property
    def hw_testplans(self):
        """
        Test plans for hardware testing
        @rtype: C{list} of C{str}
        """
        if len(self._hw_testplans) > 0:
            if not isinstance(self._hw_testplans[0], StringIO):
                self._hw_testplans = self._convert_testplans(self._hw_testplans)
        return self._hw_testplans

    @property
    def host_testplans(self):
        """
        Test plans for host testing
        @rtype: C{list} of C{str}
        """
        if len(self._host_testplans) > 0:
            if not isinstance(self._host_testplans[0], StringIO):
                self._host_testplans = \
                    self._convert_testplans(self._host_testplans)
        return self._host_testplans

    @property
    def chroot_packages(self):
        """
        Packages for chroot testing
        @rtype: C{list} of C{str}
        """
        return string_2_list(self._chroottest)

    @property
    def testplan_id(self):
        """
        The Testplan id
        @rtype: C{str}
        """
        return self._plan

    @property
    def device_properties(self):
        """
        A dictionary of device properties this testrun requires
        @rtype: C{dict}
        """
        ret_val = {}
        if self._device is not None:
            if isinstance(self._device, dict):
                ret_val = self._device
            else:
                ret_val = string_2_dict(self._device)
        return ret_val

    @property
    def emmc(self):
        """
        Url to the additional content image (memory card image)
        @rtype: C{str}
        """
        return self._emmc

    @property
    def distribution_model(self):
        """
        The name of the Distribution Model
        @rtype: C{str}
        """
        return self._distribution_model

    @property
    def flasher(self):
        """
        The URL of the flasher
        @rtype: C{str}
        """
        return self._flasher

    @property
    def flasher_options(self):
        """
        Custom flasher options
        @rtype: C{string}
        """
        return self._flasher_options

    @property
    def testfilter(self):
        """
        The test filter string for testrunner-lite
        @rtype: C{str}
        """
        if self._testfilter is not None:
            testfilter = self._testfilter.replace('"', "'")
            return "\"%s\"" % testfilter

    @property
    def use_libssh2(self):
        """
        testrunner-lite libssh2 support
        @rtype: C{boolean}
        """
        return self._use_libssh2

    @property
    def resume(self):
        """
        testrunner-lite resume functionality
        @rtype: C{boolean}
        """
        return self._resume

    @property
    def timeout(self):
        """
        Test execution timeout in minutes
        @rtype: C{int}
        """
        if self._timeout is None:
            self._timeout = 0
        return int(self._timeout)

    ############################
    # HELPERS
    ############################

    @staticmethod
    def _is_valid_suffix(package):
        """
        @type package: C{str}
        @param package: The package name
        """
        return any(map(package.endswith, VALID_PKG_SUFFIXES))

    @staticmethod
    def _validate_distribution_models(distribution_model, packages):
        """
        Checks that all required options for given distribution model are
        defined. Raises ValueError if something is missing.

        @type distribution_model: C{str}
        @param distribution_model: Name of the distribution model

        @type packages: C{str}
        @param packages: Testpackage names separated by comma

        """
        # Check that packages are defined if "perpackage" distribution is used
        if distribution_model == 'perpackage' and len(packages) == 0:
            error_msg = "Test packages must be defined for specified "\
                + "distribution model '%s'" % distribution_model
            raise ValueError(error_msg)

    def _validate_packages(self, packages):
        """
        Checks that given testpackages match our naming definitions

        Raises ValueError if invalid packages given

        @type packages: C{List} consiting of C{str}
        @param packages: List of test package names
        """
        invalid_packages = [pkg for pkg in packages
                              if not self._is_valid_suffix(pkg)]
        if invalid_packages:
            pretty_packages = ', '.join(invalid_packages)
            error_msg = "Invalid testpackage(s): %s" % pretty_packages
            raise ValueError(error_msg)
    
    def _convert_testplans(self, test_plans):
        """
        Converts list of test plans to StringIO.
        
        @type test_plans: C{list} of C{tuple}
        @param test_plans: List of test plans
        
        @rtype: C{List} of C{StringIO}
        @return: List of test plans as StringIO
        
        """
        ret_list = []
        for (plan_name, plan_data) in test_plans:
            data = StringIO(plan_data)
            data.name = plan_name
            ret_list.append(data)
        return ret_list
    
    @staticmethod
    def format_dict(options_dict):
        """
        Makes options dictionary to look nice. Replaces
        test plans from the options.
        
        @type options_dict: C{dict}
        @param options_dict: Dictionary of options
        
        @rtype: C{dict}
        @return: Returns nice dictionary
        """
        
        format_options = deepcopy(options_dict)
        if "host_testplans" in format_options:
            test_plans_data = format_options.get("host_testplans")
            test_plans = []
            for plan_name, plan_data in test_plans_data:
                test_plans.append(plan_name)
            format_options["host_testplans"] = test_plans
        if "hw_testplans" in format_options:
            test_plans_data = format_options.get("hw_testplans")
            test_plans = []
            for plan_name, plan_data in test_plans_data:
                test_plans.append(plan_name)
            format_options["hw_testplans"] = test_plans
        return format_options

    @staticmethod
    def _validate_chroot(rootstrap, chroot_packages):
        """
        Checks that all required options for chroot are
        defined. Raises ValueError if something is missing.

        @type rootstrap: C{str}
        @param rootstrap: rootstrap URL

        @type packages: C{str}
        @param packages: chroot testpackage names

        @raise ValueError: rootstrap or chroot packages missing.
        """
        # Check that chroot packages and rootstrap are defined if
        # "chroot" is used
        if bool(rootstrap) != bool(chroot_packages):
            error_msg = "When testing on chroot both rootstrap and " \
                + "chroot packages needs to be defined."
            raise ValueError(error_msg)
