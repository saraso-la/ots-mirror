# -*- coding: utf-8 -*-
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

"""General helper methods, classes etc."""

import os
import shlex
import logging

def get_logger_adapter(logger_name):
    """
    Returns the logger adapter for logging with 'userDefinedId' parameter,
    which is the same as OTS worker number, device id and HAT control USB
    port number.
    """
    device_n = os.getenv("OTS_WORKER_NUMBER")
    return logging.LoggerAdapter(logging.getLogger(logger_name),
                                 {'userDefinedId': device_n})
