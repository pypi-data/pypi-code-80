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
from freeclimb.models.filter_logs_request import FilterLogsRequest  # noqa: E501
from freeclimb.rest import ApiException


class TestFilterLogsRequest(unittest.TestCase):
    """FilterLogsRequest unit test stubs"""

    def setUp(self):
        self.filter_logs_request = FilterLogsRequest(pql='fake_pql')

    def tearDown(self):
        pass

    def testFilterLogsRequest(self):
        """Test FilterLogsRequest"""
        # construct object with mandatory attributes with example values
        # model = freeclimb.models.filter_logs_request.FilterLogsRequest()  # noqa: E501
        self.assertTrue(isinstance(self.filter_logs_request, FilterLogsRequest))


if __name__ == '__main__':
    unittest.main()
