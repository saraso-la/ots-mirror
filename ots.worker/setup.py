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

import os.path; j = os.path.join
import sys

from setuptools import setup, find_packages

if sys.prefix.startswith("/usr") or sys.prefix == "/":
    data_prefix="/" #install data and config files relative to root
else:
    data_prefix=sys.prefix #we are inside virtualenv, so install files relative to it
    

setup(
    name = "ots.worker",
    author = "teemu.vainio@ixonos.com",
    version = "0.1.5",
    include_package_data = True,
    namespace_packages = ['ots'],
    packages = find_packages(),
    zip_safe = False,
    entry_points={"console_scripts": 
                  ["ots_worker = ots.worker.worker:main",
                   "conductor = ots.worker.conductor.conductor:main",
                   # For backward compatibility:
                   "kickstart = ots.worker.conductor.conductor:main"]},
    data_files=[(j(data_prefix,'etc'), ['ots.ini', 'ots/worker/conductor/conductor.conf']),
                (j(data_prefix,'etc/conductor'), [])]
    )
