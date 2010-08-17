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

from ots.server.distributor.api import OtsGlobalTimeoutError
from ots.server.testrun.testrun import Testrun, TestrunException 
from ots.server.testrun.tests.mock_taskrunner import MockTaskRunnerResults
from ots.server.testrun.tests.mock_taskrunner import MockTaskRunnerTimeout
from ots.server.testrun.tests.mock_taskrunner import MockTaskRunnerError

from ots.server.results.api import TestrunResult

class TestTestrun(unittest.TestCase):

    def test_run_results(self):
        mock_task_runner = MockTaskRunnerResults()
        run_test = mock_task_runner.run
        testrun = Testrun(run_test)
        ret_val = testrun.run()
        self.assertEquals(2, len(testrun.results)) 
        self.assertEquals("test_1", testrun.results[0].name())
        self.assertEquals("test_2", testrun.results[1].name())
        self.assertEquals(TestrunResult.FAIL, ret_val)

    def test_run_global_timeout(self):
        #Not really a test more an illustration of behaviour
        mock_task_runner = MockTaskRunnerTimeout()
        run_test = mock_task_runner.run 
        testrun = Testrun(run_test)
        self.assertRaises(OtsGlobalTimeoutError, testrun.run)

    def test_run_model_taskrunner_error(self):
        mock_task_runner = MockTaskRunnerError()
        run_test = mock_task_runner.run
        testrun = Testrun(run_test)
        self.assertRaises(TestrunException, testrun.run)
        
if __name__ == "__main__":
    unittest.main()