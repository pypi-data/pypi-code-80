import pytest
from unittest import TestCase
import os
from acme_news.engines.russia_today import RussiaToday
from typing import List, Dict

class TestRussiaToday(TestCase):

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_parse_content(self):
        rt = RussiaToday(query='Iraq')
        results: List[Dict] = rt.parse_rt_contents()
        return self.assertEqual(10, len(results))

    @pytest.mark.skipif(os.getenv('BITBUCKET_BRANCH') == 'develop' or os.getenv('BITBUCKET_BRANCH') == 'master',
                        reason='Local Test')
    def test_rt_bulk_quries(self):
        rt = RussiaToday(query='Iraq', content_type='Telecast')
        results: List[Dict] = rt.rt_bulk_quries(page=2, page_size=10)
        return self.assertEqual(10, len(results ))
