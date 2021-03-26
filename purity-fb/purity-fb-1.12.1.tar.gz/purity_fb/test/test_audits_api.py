# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.9 Python SDK

    Pure Storage FlashBlade REST 1.9 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.9
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import purity_fb_1dot9
from purity_fb_1dot9.rest import ApiException
from purity_fb_1dot9.apis.audits_api import AuditsApi


class TestAuditsApi(unittest.TestCase):
    """ AuditsApi unit test stubs """

    def setUp(self):
        self.api = purity_fb_1dot9.apis.audits_api.AuditsApi()

    def tearDown(self):
        pass

    def test_list_audits(self):
        """
        Test case for list_audits

        
        """
        pass


if __name__ == '__main__':
    unittest.main()
