from .constants import SESSION, REMOTE
from datetime import datetime
from json import loads, dumps


def create(feed, indicator, tags, description, **kwargs):
    user, feed = feed.split('/')
    uri = REMOTE + f'/users/{user}/feeds/{feed}/indicators'

    rv = SESSION.post(uri, data=dumps({
        'indicator': indicator,
        'tags': tags,
        'description': description,
        'portlist': kwargs.get('portlist'),
        'count': kwargs.get('count', 1),
        'last_at': kwargs.get('last_at', datetime.now().isoformat())
    }))
    if rv.status_code == 500:
        raise ConnectionError('Something is wrong on the server end')

    return loads(rv.text)
