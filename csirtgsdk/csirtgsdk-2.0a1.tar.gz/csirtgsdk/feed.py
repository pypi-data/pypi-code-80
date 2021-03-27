from json import loads
from .constants import SESSION, REMOTE


def get(q: str, limit: int = 250) -> dict:
    q = q.split('/')
    q = f"{REMOTE}/users/{q[0]}/feeds/{q[1]}?limit={limit}"
    rv = SESSION.get(q)
    if rv.status_code != 200:
        raise ConnectionError('Something is wrong on the server end')

    return loads(rv.text)


def create(user: str, name:str , description:str = None) -> dict:
    uri = REMOTE + f'/users/{user}/feeds'
    rv = SESSION.post(uri, {
        'feed': {
            'name': name,
            'description': description
        }
    })
    return loads(rv.text)
