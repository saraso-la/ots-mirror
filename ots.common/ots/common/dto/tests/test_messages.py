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

import ots.common

from ots.common.dto.messages import CommandMessage, StateChangeMessage
from ots.common.amqp.codec import pack_message, unpack_message
from StringIO import StringIO

class TestMessages(unittest.TestCase):

    def test_command_message(self):
        cmd_msg = CommandMessage(["echo", "hello world"], 
                                  "response_queue", "task_id", 
                                  xml_file = StringIO("foo bar")) 
        packed_msg = pack_message(cmd_msg)
        rec_msg = unpack_message(packed_msg)
        self.assertEquals("echo hello world", rec_msg.command)
        self.assertEquals("response_queue", rec_msg.response_queue)
        self.assertEquals("task_id", rec_msg.task_id)
        self.assertTrue(isinstance(rec_msg.xml_file, StringIO))
        self.assertEquals(ots.common.__VERSION__, rec_msg.__version__)

    def test_state_change_message_start(self):
        state_msg = StateChangeMessage(1, 'start')
        self.assertTrue(state_msg.is_start)
        self.assertFalse(state_msg.is_finish)

    def test_state_change_message_finish(self):
        state_msg = StateChangeMessage(1, 'finish')
        self.assertTrue(state_msg.is_finish)
        self.assertFalse(state_msg.is_start)


if __name__ == "__main__":
    unittest.main()
