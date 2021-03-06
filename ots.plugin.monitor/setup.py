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
      name="ots.plugin.monitor",
      author="meego-qa@lists.meego.com",
      namespace_packages=["ots", "ots.plugin"],
      version=get_spec_version(),
      include_package_data=True,
      packages=find_packages(),
      install_requires=['ots.django'],
      entry_points={"ots.publisher_plugin":
                    ["publisher_klass = "\
                     "ots.plugin.monitor.monitor_plugin:MonitorPlugin"]},
      data_files=\
        [('/usr/share/ots/plugin/monitor', \
          ['ots/plugin/monitor/templates/monitor/index.html',
           'ots/plugin/monitor/templates/monitor/group_details_view.html',
           'ots/plugin/monitor/templates/monitor/requestor_details.html',
           'ots/plugin/monitor/templates/monitor/testrun_details.html',
           'ots/plugin/monitor/templates/monitor/testrun_list.html',
           'ots/plugin/monitor/templates/monitor/monitor_base.html', ]),
           ]
      )
