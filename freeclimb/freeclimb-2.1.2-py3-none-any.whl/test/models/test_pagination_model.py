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
from freeclimb.models.pagination_model import PaginationModel  # noqa: E501
from freeclimb.rest import ApiException


class TestPaginationModel(unittest.TestCase):
    """PaginationModel unit test stubs"""

    def setUp(self):
        self.pagination_model = PaginationModel()

    def tearDown(self):
        pass

    def testPaginationModel(self):
        """Test PaginationModel"""
        # construct object with mandatory attributes with example values
        # model = freeclimb.models.pagination_model.PaginationModel()  # noqa: E501
        self.assertTrue(isinstance(self.pagination_model, PaginationModel))


if __name__ == '__main__':
    unittest.main()
