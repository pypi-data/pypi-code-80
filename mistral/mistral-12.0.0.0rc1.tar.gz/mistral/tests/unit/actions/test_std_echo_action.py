# Copyright 2014 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from mistral.actions import std_actions as std
from mistral.tests.unit import base
from unittest import mock


class EchoActionTest(base.BaseTest):
    def test_fake_action(self):
        expected = "my output"
        mock_ctx = mock.Mock()
        action = std.EchoAction(expected)

        self.assertEqual(expected, action.run(mock_ctx))
