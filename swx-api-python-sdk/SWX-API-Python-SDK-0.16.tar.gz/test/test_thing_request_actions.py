"""
    Digital Model API (WIP)

    Digital Model API documentation  # noqa: E501

    The version of the OpenAPI document: 0.8.12
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import swx_sdk
from swx_sdk.model.action_delay import ActionDelay
from swx_sdk.model.action_reboot import ActionReboot
globals()['ActionDelay'] = ActionDelay
globals()['ActionReboot'] = ActionReboot
from swx_sdk.model.thing_request_actions import ThingRequestActions


class TestThingRequestActions(unittest.TestCase):
    """ThingRequestActions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testThingRequestActions(self):
        """Test ThingRequestActions"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ThingRequestActions()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
