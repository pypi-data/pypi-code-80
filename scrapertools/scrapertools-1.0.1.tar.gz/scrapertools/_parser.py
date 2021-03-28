from abc import ABC

import bs4

from scraper import _util as util


__all__ = ["Parser"]


class Parser(bs4.BeautifulSoup, ABC):

    url = None

    def __init__(self, markup, features="lxml", **kw):
        super().__init__(markup, features, **kw)

    def save_file(self):
        util.save_to_file(self)

    def generate_filename(self):
        return util.filename_from_url(self.url)
