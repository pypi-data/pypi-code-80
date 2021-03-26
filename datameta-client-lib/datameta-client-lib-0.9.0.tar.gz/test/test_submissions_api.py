"""
    DataMeta

    DataMeta  # noqa: E501

    The version of the OpenAPI document: 0.9.0
    Contact: leon.kuchenbecker@uni-tuebingen.de
    Generated by: https://openapi-generator.tech
"""


import unittest

import datameta_client_lib
from datameta_client_lib.api.submissions_api import SubmissionsApi  # noqa: E501


class TestSubmissionsApi(unittest.TestCase):
    """SubmissionsApi unit test stubs"""

    def setUp(self):
        self.api = SubmissionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_submission(self):
        """Test case for create_submission

        Create a New Submission  # noqa: E501
        """
        pass

    def test_get_group_submissions(self):
        """Test case for get_group_submissions

        Get A List of All Submissions of A Group.  # noqa: E501
        """
        pass

    def test_prevalidate_submission(self):
        """Test case for prevalidate_submission

        Pre-validate a submission  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
