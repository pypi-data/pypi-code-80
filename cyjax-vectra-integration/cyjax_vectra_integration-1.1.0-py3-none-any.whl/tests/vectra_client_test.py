import unittest

import responses

from src.vectra_client import VectraClient


class VectraClientTest(unittest.TestCase):

    def setUp(self):
        self.vectra_client = VectraClient('brain.vectra-fqdn.com', 'test-vectra-key', ('feed-1', 'feed-2'))

    @responses.activate
    def test_send_daily_indicator_file(self):
        responses.add(responses.POST, 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-1',
                      status=200,
                      headers={'Authorization': 'token test-vectra-key'})

        self.vectra_client.send_daily_indicators('tests/indicators.xml')

        assert len(responses.calls) == 1
        assert responses.calls[
                   0].request.url == 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-1'
        assert responses.calls[0].request.headers['Authorization'] == 'token test-vectra-key'

    @responses.activate
    def test_send_weekly_indicator_file(self):
        responses.add(responses.POST, 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-2',
                      status=200,
                      headers={'Authorization': 'token test-vectra-key'})

        self.vectra_client.send_weekly_indicators('tests/indicators.xml')

        assert len(responses.calls) == 1
        assert responses.calls[
                   0].request.url == 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-2'
        assert responses.calls[0].request.headers['Authorization'] == 'token test-vectra-key'

    @responses.activate
    def test_health(self):
        responses.add(responses.GET, 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-1',
                      status=200,
                      headers={'Authorization': 'token test-vectra-key'})

        self.vectra_client.health()

        assert len(responses.calls) == 1
        assert responses.calls[
                   0].request.url == 'https://brain.vectra-fqdn.com/api/v2.1/threatFeeds/feed-1'
        assert responses.calls[0].request.headers['Authorization'] == 'token test-vectra-key'
