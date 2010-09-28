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

from ots.common.dto.results import Results

class TestResults(unittest.TestCase):

    def test_results(self):
        results = Results("foo", "<result>pass</result>",
                          package = "pkg1", 
                          hostname = "unittest", 
                          environment = "meego")
        self.assertEquals("foo", results.results_xml.name)
        self.assertEquals("<result>pass</result>",
                          results.results_xml.read())
        
if __name__ == "__main__":
    unittest.main()