""" Test Search service """
import time
from understatapi.endpoints.player import PlayerEndpoint
import unittest
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from understatapi.services import Search
from selenium.webdriver import Firefox


@unittest.skip("temp")
class TestSearch(unittest.TestCase):
    """ Test `Search` service """

    def setUp(self):
        """ setUp """
        self.search = Search(player_name="Ronaldo", session=requests.Session())

    def tearDown(self):
        self.search.browser.quit()

    def test_get_player_ids(self):
        """ test `request_url()` """
        self.assertListEqual(
            self.search.get_player_ids(), ["2371", "2028", "7097"]
        )

    def test_get_player_id_from_url(self):
        """ test `get_player_id_from_url()` """
        self.assertEqual(
            self.search._get_player_id_from_url(
                "https://understat.com/player/2371"
            ),
            "2371",
        )


class TestSearchContextManager(unittest.TestCase):
    """
    Test that `Search` has the functionality to be used as a context manager
    """

    def test_context_manager(self):
        """ Test that `Search` works as a context manager """
        pass
