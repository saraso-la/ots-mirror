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
Module containing utilities for multiprocessing support
"""

from multiprocessing import Process


class ProcessHandler(object):
    """
    Handles adding, starting joining of multiple processes.
    """
    def __init__(self):
        super(ProcessHandler, self).__init__()
        self.child_processes = []

    def add_process(self, target_func, *args):
        """
        Add child process instances

        @param target_func: Function where child process starts execution
        @type target_func: C{function}

        @param args: arguments for target function
        @type args: C{args}
        """

        self.child_processes.append(Process(target=target_func, \
                                    args=(args[0])))

    def start_processes(self):
        """
        Starts child process instances
        """
        for process in self.child_processes:
            process.start()

    def join_processes(self):
        """
        Joins child process instances
        """
        for process in self.child_processes:
            process.join()

