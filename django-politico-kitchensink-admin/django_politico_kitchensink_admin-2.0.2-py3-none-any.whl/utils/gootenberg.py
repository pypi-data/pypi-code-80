from kitchensink.conf import settings
import requests
import json


def gootenberg(path, data):
    if not settings.GOOTENBERG_ENDPOINT:
        raise KeyError('Gootenberg API not set up in settings')

    if not settings.GOOTENBERG_TOKEN:
        raise KeyError('Gootenberg API token not set up in settings')

    url = '{}{}'.format(settings.GOOTENBERG_ENDPOINT, path)
    headers = {
        'Authorization': 'Token {}'.format(settings.GOOTENBERG_TOKEN)
    }

    resp = requests.post(
        url,
        data=json.dumps(data),
        headers=headers
    )

    if resp.status_code == 200:
        return resp

    else:
        error = resp.text
        raise RuntimeError('Gootenberg: {}'.format(error))
