# coding: utf-8

"""
    Planetary Data System API

    Federated PDS API which provides actionable end points standardized between the different nodes.   # noqa: E501

    The version of the OpenAPI document: 0.0
    Contact: pds-operator@jpl.nasa.gov
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pds_api_client
from pds_api_client.models.capability import Capability  # noqa: E501
from pds_api_client.rest import ApiException

class TestCapability(unittest.TestCase):
    """Capability unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Capability
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pds_api_client.models.capability.Capability()  # noqa: E501
        if include_optional :
            return Capability(
                action = '0', 
                version = '0'
            )
        else :
            return Capability(
                action = '0',
                version = '0',
        )

    def testCapability(self):
        """Test Capability"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
