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
Runs an OTS Testrun 

Provides a thin wrapper around the DTOHandler 

Adds it's value by 
  1. Checking the validity of the Run
  2. The Go / NoGo return value


At present the callable run_test needs setting 
prior to the run 
"""

import logging

from ots.results.api import TestrunResult
from ots.results.api import is_valid_run
from ots.results.api import go_nogo_gauge

from ots.server.hub.dto_handler import DTOHandler

LOG = logging.getLogger(__name__)

class Testrun(object):
    """
    Run a Testrun and return results
    """

    def __init__(self, is_hw_enabled = True,
                       is_host_enabled = False,
                       is_chroot_enabled = False,
                       insignificant_tests_matter = True):
        """"
        @type is_hw_enabled: C{bool} 
        @param is_hw_enabled: Flag

        @type is_host_enabled: C{bool}
        @param is_host_enabled: Flag

        @type is_chroot_enabled: C{bool}
        @param is_chroot_enabled: Flag

        @type insignificant_tests_matter: C{bool} 
        @param insignificant_tests_matter: Flag
        """
       
        self._dto_handler = DTOHandler()
        #
        self.run_test = None
        #
        self.is_hw_enabled = is_hw_enabled
        self.is_host_enabled = is_host_enabled
        self.is_chroot_enabled = is_chroot_enabled
        self.insignificant_tests_matter = insignificant_tests_matter
        self.results = []

    def _results_xmls_iter(self):
        """
        Iterates all results xmls
        """
        for result in self.results:
            if result.is_result_xml:
                yield result.data
        
    ###########################
    # DELEGATES
    ###########################

    @property 
    def expected_packages(self):
        """
        The Test Packages that should have been run
        @rtype: C{ots.common.dto.packages}
        """
        return self._dto_handler.expected_packages

    @property 
    def exceptions(self):
        """
        Exceptions raised during testrun
        @rtype: C{list} of C{Exception}
        """
        return self._dto_handler.exceptions

        
    @property
    def tested_packages(self):
        """
        The Test Packages that were run
        @rtype: C{ots.common.dto.packages}
        """
        return self._dto_handler.tested_packages
        
    @property
    def monitors(self):
        """
        The Monitors
        @rtype: C{list} of C{ots.common.dto.monitor}
        """
        return self._dto_handler.monitors

    #############################
    # RUN
    #############################
    
    def run(self):
        """
        Blocking call returns when test completed

        @rtype: L{ots.results.api.TestrunResult}
        @return: The Go / NoGo result of the run
        """
        ret_val = TestrunResult.FAIL
        if self.run_test is not None:
            self.run_test()

            # At this point distributor has already finished so it's safe to
            # re-raise the exceptions from worker side
            if self.exceptions:
                raise self.exceptions[0]

            is_valid_run(self.expected_packages,
                         self.tested_packages,
                         self.is_hw_enabled,
                         self.is_host_enabled,
                         self.is_chroot_enabled)
            self.results = self._dto_handler.results
            result_xmls = list(self._results_xmls_iter())
            ret_val = go_nogo_gauge(result_xmls,
                                    self.insignificant_tests_matter)
        if ret_val:
            LOG.debug("Testrun Passed")
        else:
            LOG.debug("Testrun Failed")
        return ret_val
