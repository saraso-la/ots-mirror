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


# Disabling "unused import" warning because this is an API file.
# pylint: disable=W0611

"""
Defines the ots.server.distributor API
"""
# Taskrunner related API

from ots.server.distributor.taskrunner import TaskRunner
from ots.server.distributor.taskrunner_factory import taskrunner_factory
from ots.server.distributor.dto_signal import DTO_SIGNAL

# Exceptions

from ots.server.distributor.exceptions import OtsQueueDoesNotExistError, \
     OtsExecutionTimeoutError, OtsQueueTimeoutError
