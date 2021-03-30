import os
import re
import math
import unittest
from ahapy import AhaV1

# To run tests, cd into package directory and the run the following:
# python -m unittest

AHA_KEY = os.environ.get('AHA_API_KEY')

class TestClient(unittest.TestCase):

    def test_v1_query(self):
        aha = AhaV1('enverus', AHA_KEY)
        data = aha.query('initiatives')
        self.assertIsNotNone(data)


    def test_v1_count(self):
        aha = AhaV1('enverus', AHA_KEY)
        count = aha._count('epics')
        self.assertGreater(count, -1)


    def test_v1_fields(self):
        aha = AhaV1('enverus', AHA_KEY)
        data = aha.query('initiatives', fields='name,id')
        for i in data:
            self.assertIsNotNone(i['name'])


    def test_v1_page(self):
        aha = AhaV1('enverus', AHA_KEY)
        aha.query('initiatives', per_page=200)
        expected_pages = math.ceil(aha.count / 200)
        self.assertEqual(expected_pages, aha.total_pages)


    def test_v1_endpoint_parse_1(self):
        aha = AhaV1('enverus', AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives/12345/epics')
        self.assertEqual('epics', endpoint)


    def test_v1_endpoint_parse_2(self):
        aha = AhaV1('enverus', AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives/12345')
        self.assertEqual('initiatives', endpoint)


    def test_v1_endpoint_parse_3(self):
        aha = AhaV1('enverus', AHA_KEY)
        endpoint = aha._parse_endpoint_arg('initiatives')
        self.assertEqual('initiatives', endpoint)


