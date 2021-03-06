# ***** BEGIN LICENCE BLOCK *****
# This file is part of OTS
#
# Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
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

from setuptools import setup, find_packages
from get_spec_version import get_spec_version

setup(
      name="ots.tools",
      description="Various helper tools for OTS",
      author="meego-qa@lists.meego.com",
      version=get_spec_version(),
      include_package_data=True,
      namespace_packages=['ots'],
      packages=find_packages(),
      zip_safe=False,
      data_files=[('/usr/share/ots/trigger', ['ots/tools/trigger/ots_trigger_example.conf'])],
      entry_points={
                    "console_scripts":
                    ["ots_trigger = ots.tools.trigger.ots_trigger:main",
                     "ots_empty_queue = ots.tools.queue_management.empty_queue:main",
                     "ots_delete_queue = ots.tools.queue_management.delete_queue:main",
                     ],
                   },
      )
