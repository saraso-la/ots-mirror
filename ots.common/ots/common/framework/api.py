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

""" Common OTS framework API functions """

# API file, ignoring Unused import unpack_message 
# pylint: disable=W0611

from ots.common.framework.load_plugins import plugins_iter
from ots.common.framework.publisher_plugin_base import PublisherPluginBase
from ots.common.framework.conductor_plugin_base import ConductorPluginBase
from ots.common.framework.plugin_exception_policy import plugin_exception_policy
from ots.common.framework.flasher_plugin_base import FlasherPluginBase
from ots.common.framework.flasher_plugin_base import FlashFailed
from ots.common.framework.flasher_plugin_base import InvalidImage
from ots.common.framework.flasher_plugin_base import InvalidConfig
from ots.common.framework.flasher_plugin_base import ConnectionTestFailed
from ots.common.framework.flasher_plugin_base import BootupFailed
