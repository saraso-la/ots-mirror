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
File for django urls
"""

# Ignoring naming pattern
# pylint: disable=C0103

from django.conf.urls.defaults import patterns, include, handler500, handler404

from ots.plugin.monitor.views import main_page
from ots.plugin.monitor.views import view_group_details
from ots.plugin.monitor.views import view_testrun_list
from ots.plugin.monitor.views import view_testrun_details
from ots.plugin.monitor.views import view_requestor_details


urlpatterns = patterns('',
    (r'^view/$', main_page),
    (r'^view/group/(?P<devicegroup>[^/]+)/$',view_group_details),
    (r'^view/testruns/$', view_testrun_list),
    (r'^view/testrun/(?P<testrun_id>\w+)/$', view_testrun_details),
    (r'^view/testruns/(?P<requestor>[^/]+)/$',view_requestor_details),
)
