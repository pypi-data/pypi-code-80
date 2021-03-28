import datetime
import logging
import os
import pickle

import requests

from . import _ua as user_agent
from ._parser import Parser

__all__ = ["Session", "user_agent"]


SESSION_SAVE_DATEFMT = "%Y%m%d%H%M"

logger = logging.getLogger(__name__)


class Session(requests.Session):

    _instance = None
    _cache = dict()

    @property
    def user_agent(self):
        return self.headers.get("User-Agent")

    @user_agent.setter
    def user_agent(self, ua_string):
        self.headers.update({"User-Agent": ua_string})

    def __init__(self):
        """
        Instantiates a Session

        subclass of `request.Session`
        """

        super().__init__()
        self.last_response = None
        self.user_agent = user_agent.GENERIC_WEBKIT

    def fetch(self, url):
        """
        Fetches body from url only
        Args:
            url:

        Returns: str

        """
        parsed = Parser(self.get(url).content)
        parsed.url = url
        parsed.session = self
        return parsed

    def fetch_bytes(self, url):
        """
        Fetches body (raw binary) from url only
        Args:
            url:

        """
        return self.get(url).content

    def retrieve(self, url, save_path=None):
        """
        Saves url content to file
        if no save_path is given, a filename will be generated
        according to the url

        Args:
            url:
            save_path:

        Returns:

        """
        from ._util import save_to_file

        data = self.fetch_bytes(url)
        save_to_file(data, filename=save_path, url=url)

    def request(self, method, url, **kw):
        try:
            self.last_response = self.__class__._cache[url]
            logger.info("loaded %s from cache" % url)
        except KeyError:
            pass
        self.last_response = super().request(method, url, **kw)
        return self.last_response

    def save_state(self, path=None):
        if path is None:
            path = "%s.session" % datetime.datetime.now().strftime(SESSION_SAVE_DATEFMT)
        with open(path, "w+b") as fs:
            pickle.dump(self.__dict__, fs)

    @classmethod
    def load_state(cls, path=None):
        if not path:
            try:
                files = [
                    file.split(".state")[0]
                    for file in os.listdir(os.path.abspath(os.curdir))
                    if file.endswith(".state")
                ]
                newest = max(files)
                path = "%s.state" % newest

            except Exception as e:
                logger.warning("no saved sessions found. %s " % e)
                return Session()
        with open(path, "r+b") as fs:
            rv = cls()
            rv.__dict__ = pickle.load(fs)
            return rv
