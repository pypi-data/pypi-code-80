from __future__ import annotations

import json
import logging
import re
import typing

import unicodedata

from ._session import Session

# from ._parser import Parser

logger = logging.getLogger(__name__)


def fetch(url):
    with Session() as s:
        return s.fetch(url)


def load_session(fn=None):
    return Session.load(path=fn)


def save_session(fn=None):
    if Session._instance is not None:
        Session._instance.save(path=fn)


def filename_from_url(url, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    if url is None:
        raise ValueError(
            "cannot convert %s to a filename, please provide a string like value" % url
        )
    value = str(url)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]+", "_", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def save_to_file(data, url=None, filename=None):
    """
    saves Parser instance content as html file
    Args:
        html:
        filename:

    Returns:

    """
    if not filename:
        if not url:
            raise ValueError(
                "html parser object has no url attribute or the attribute is set to None"
            )
        filename = filename_from_url(url)

    with open(filename, "w+b") as fh:
        fh.write(data)
    logger.info("saved to %s" % filename)


def absolutify_m3u8(m3u8_url):
    import m3u8

    playlist = m3u8.load(m3u8_url)
    while getattr(playlist, "playlists", None):
        for pl in playlist.playlists:
            pl.uri = pl.absolute_uri
        best_stream = max(playlist.playlists, key=lambda o: o.stream_info.resolution[0])
        return absolutify_m3u8(best_stream.absolute_uri)
    for seg in playlist.segments:
        seg.uri = seg._base_uri + "/" + seg.uri
    return playlist.dumps()


class udict(dict):
    """
    Just a utility class which can be accessed by attribute while also by json-serialized.
    """

    def __init__(self, *a, **kw):
        """
        Args:
            *a:
            **kw:
        """
        super(udict, self).__init__(*a, **kw)
        for k in self:
            dict.__setitem__(self, k, self._wrap(self[k]))
        # self.__dict__ = self

    def _wrap(self, val):
        """
        Args:
            val:

        Returns:
        """
        print("_wrap", (type(val), val))

        if isinstance(val, (dict, udict)):
            return self.__class__(val)

        elif hasattr(val, "__iter__") and not isinstance(
            val,
            (
                str,
                bytes,
            ),
        ):
            return [self._wrap(i) for i in val]
        object.__setattr__(self, "__dict__", self)
        return val

    def __setattr__(self, key, value):
        print("setattr", key, value)
        value = self._wrap(value)
        dict.__setitem__(self, key, value)

    def __setitem__(self, key, value):
        print("setitem", key, value)
        value = self._wrap(value)
        dict.__setitem__(self, key, value)

    def __getattr__(self, attr):
        print("getattr", attr)
        return super().__getitem__(attr)

    def __getitem__(self, attr):
        print("getitem", attr)
        return super().__getitem__(attr)

    def __getattribute__(self, item):
        if item == "__wrapped__":
            # debug needed
            return None

        retval = object.__getattribute__(self, item)

        print(
            "udict.__getattribute__(%s) is found: %s (%s)"
            % (item, retval, hex(id(retval)))
        )

        # this makes sure not every node is fully recursed
        return retval
        # return super().__getattribute__(item)

    def __dir__(self):
        return list(self.keys()) + list(super().__dir__())

    def __repr__(self):
        return json.dumps(self, indent=1)


class dictobject(dict):
    def __init__(self, *a, **kw):
        super(dictobject, self).__init__(*a, **kw)
        for k in self:
            dict.__setitem__(self, k, wrap(self[k], self))

    def __getattr__(self, name):
        try:
            retval = self[name]
            return retval
        except Exception:
            raise AttributeError()

    def __setattr__(self, name, value):
        try:
            self[name] = value
        except Exception:
            raise AttributeError()

    def __delattr__(self, name):
        del self[name]

    def __getitem__(self, item):
        return super(dictobject, self).__getitem__(item)

    def __setitem__(self, key, value):
        super(dictobject, self).__setitem__(key, wrap(value, self))

    def __dir__(self):
        # return set(super().__dir__()) | set(super().keys())
        return set(super().__dir__()) | set(super().keys())

    def __getattribute__(self, item):
        retval = object.__getattribute__(self, item)
        return retval

    @property
    def allkeys(self):
        return set(self.keys())

    @property
    def allvalues(self):
        return set(self.values())

    def __repr__(self):
        return json.dumps(self, indent=4)

    # def keys(self):
    #     return dict.keys(self)


def wrap(item, instance):
    if isinstance(item, typing.Mapping):
        return instance.__class__(item)
    if isinstance(item, typing.Sequence) and not isinstance(item, (str, bytes)):
        return [wrap(x, instance) for x in item]
    return item
