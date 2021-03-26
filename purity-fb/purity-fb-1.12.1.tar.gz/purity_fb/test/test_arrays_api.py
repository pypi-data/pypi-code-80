# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.2 Python SDK

    Pure Storage FlashBlade REST 1.2 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.2
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import purity_fb_1dot2
from purity_fb_1dot2.rest import ApiException
from purity_fb_1dot2.apis.arrays_api import ArraysApi


class TestArraysApi(unittest.TestCase):
    """ ArraysApi unit test stubs """

    def setUp(self):
        self.api = purity_fb_1dot2.apis.arrays_api.ArraysApi()

    def tearDown(self):
        pass

    def test_list_arrays_http_specific_performance(self):
        """
        Test case for list_arrays_http_specific_performance

        
        """
        pass

    def test_list_arrays_performance(self):
        """
        Test case for list_arrays_performance

        
        """
        pass

    def test_list_arrays_s3_specific_performance(self):
        """
        Test case for list_arrays_s3_specific_performance

        
        """
        pass

    def test_list_arrays_space(self):
        """
        Test case for list_arrays_space

        
        """
        pass


if __name__ == '__main__':
    unittest.main()
