# coding: utf-8

"""
    FreeClimb API

    FreeClimb is a cloud-based application programming interface (API) that puts the power of the Vail platform in your hands. FreeClimb simplifies the process of creating applications that can use a full range of telephony features without requiring specialized or on-site telephony equipment. Using the FreeClimb REST API to write applications is easy! You have the option to use the language of your choice or hit the API directly. Your application can execute a command by issuing a RESTful request to the FreeClimb API. The base URL to send HTTP requests to the FreeClimb REST API is: /apiserver. FreeClimb authenticates and processes your request.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import freeclimb
from freeclimb.models.set_listen import SetListen  # noqa: E501
from freeclimb.rest import ApiException

class TestSetListen(unittest.TestCase):
    """SetListen unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SetListen
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = freeclimb.models.set_listen.SetListen()  # noqa: E501
        if include_optional :
            return SetListen(
                call_id = '0', 
                listen = True
            )
        else :
            return SetListen(
                call_id = '0',
        )

    def testSetListen(self):
        """Test SetListen"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
