# coding: utf-8

"""
    FreeClimb API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import freeclimb
from freeclimb.percl.remove_from_conference import RemoveFromConference  # noqa: E501
from freeclimb.rest import ApiException


class TestRemoveFromConference(unittest.TestCase):
    """RemoveFromConference unit test stubs"""
    call_id='CA-fake-call-id'

    def setUp(self):
        self.remove_from_conference = RemoveFromConference(call_id=self.call_id)

    def tearDown(self):
        pass

    def testRemoveFromConference(self):
        """Test RemoveFromConference"""
        # construct object with mandatory attributes with example values
        # percl = freeclimb.percl.RemoveFromConference()  # noqa: E501
        self.assertTrue(isinstance(self.remove_from_conference, RemoveFromConference))
        self.assertEqual(self.call_id, self.remove_from_conference.get('RemoveFromConference').get('callId'))

if __name__ == '__main__':
    unittest.main()
