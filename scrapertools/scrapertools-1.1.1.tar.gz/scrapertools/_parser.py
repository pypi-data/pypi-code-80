from abc import ABC

import bs4

from . import _util as util


__all__ = ["Parser"]


class Parser(bs4.BeautifulSoup, ABC):

    url = None

    def __init__(self, markup, features="lxml", **kw):
        super().__init__(markup, features, **kw)

    def save_file(self, file_path=None):
        """
        saves current html as file on <file_path> or, if file_path
        is ommitted, it generates a distinctive name based on the url
        Args:
            file_path: optional string

        Returns:

        """
        util.save_to_file(self, self.url)

    def generate_filename(self):
        return util.filename_from_url(self.url)
