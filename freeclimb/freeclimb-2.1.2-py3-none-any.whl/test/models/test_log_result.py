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
from freeclimb.models.log_result import LogResult  # noqa: E501
from freeclimb.rest import ApiException


class TestLogResult(unittest.TestCase):
    """LogResult unit test stubs"""

    def setUp(self):
        self.log_result = LogResult()

    def tearDown(self):
        pass

    def testLogResult(self):
        """Test LogResult"""
        # construct object with mandatory attributes with example values
        # model = freeclimb.models.log_result.LogResult()  # noqa: E501
        self.assertTrue(isinstance(self.log_result, LogResult))


if __name__ == '__main__':
    unittest.main()
