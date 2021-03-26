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
from freeclimb.percl.enqueue import Enqueue  # noqa: E501
from freeclimb.rest import ApiException


class TestEnqueue(unittest.TestCase):
    """Enqueue unit test stubs"""
    queue_id='fake_queue_id'
    action_url='http://example.com/action'
    wait_url='http://example.com/wait'

    def setUp(self):
        self.enqueue = Enqueue(queue_id=self.queue_id, action_url=self.action_url, wait_url=self.wait_url)

    def tearDown(self):
        pass

    def testEnqueue(self):
        """Test Enqueue"""
        # construct object with mandatory attributes with example values
        # percl = freeclimb.percl.enqueue()  # noqa: E501
        self.assertTrue(isinstance(self.enqueue, Enqueue))
        self.assertEqual(self.queue_id, self.enqueue.get('Enqueue').get('queueId'))
        self.assertEqual(self.action_url, self.enqueue.get('Enqueue').get('actionUrl'))
        self.assertEqual(self.wait_url, self.enqueue.get('Enqueue').get('waitUrl'))
        self.assertTrue(hasattr(self.enqueue, 'notification_url'))

if __name__ == '__main__':
    unittest.main()
