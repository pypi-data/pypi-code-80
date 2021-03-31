import pytest
from unittest import TestCase
import os
from acme_news.engines.google_news import GoogleNewsEngine
from typing import List, Dict

class TestGoogleNews(TestCase):
    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_get_query(self):
        gnews = GoogleNewsEngine(search_query='iraq')
        results = gnews.parse_google_news_links()
        return self.assertEqual(100, len(results))
