from abc import ABC
import re
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
        util.save_to_file(self.encode(), self.url, filename=file_path)


    def generate_filename(self):
        return util.filename_from_url(self.url)


    def get_info(self) -> 'util.dictobject':
        retval = util.dictobject()
        metas = self.find_all(re.compile('meta|title|link'))
        key_props = ['name', 'rel']
        val_props = ['content', 'type', 'href']
        for meta in metas:
            for key_prop in key_props:
                try:
                    k = meta.attrs[key_prop]
                    if isinstance(k, (list,set)):
                        k = k[0]
                    if not k:
                        continue
                    retval[k] = {}
                    for val_prop in val_props:
                        try:
                            v = meta.attrs[val_prop]
                            retval[k][val_prop] = v
                        except Exception as  e1:
                            print('e1', e1)
                            continue
                except Exception as e2:
                    print('e2 ', e2)
                    continue
        return retval