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

import unittest

import os

from ots.results.validate_xml import validate_xml

class TestValidateXML(unittest.TestCase):

    def test_validate_xml(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        results_file = os.path.join(dirname, "data", "dummy_results_file.xml")
        results_xml = open(results_file, "r").read()
        validate_xml(results_xml)
        
if __name__ == "__main__":
    unittest.main()
