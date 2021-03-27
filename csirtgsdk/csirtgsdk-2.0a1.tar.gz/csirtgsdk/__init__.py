

from json import loads, dumps
from cachetools import TTLCache, cached
from pprint import pprint

from csirtgsdk.constants import HEADERS, CACHE_TTL, CACHE_MAX_SIZE, \
    REMOTE, TOKEN, SESSION

from .feed import create as create_feed, get as get_feed
from .indicator import create as create_indicator


@cached(TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL))
def search(q):
    rv = SESSION.get(REMOTE + '/search' + '?q=' + q)
    if rv.status_code != 200:
        raise ConnectionError('Something is wrong on the server end')

    return loads(rv.text)


@cached(TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL))
def risk(q, v=False):
    if v:
        v = '1'
    else:
        v = '0'

    rv = SESSION.get(REMOTE + '/risk', params={'q': q, 'v': v})
    if rv.status_code != 200:
        raise ConnectionError('Something is wrong on the server end')

    return loads(rv.text)