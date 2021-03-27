import os.path

from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

from .utils import requests_retry_session

API_VERSION = os.getenv('CSIRTG_API_VERSION', '2')

REMOTE = 'https://csirtg.io/api'
REMOTE = os.getenv('CSIRTG_REMOTE', REMOTE)

TOKEN = os.getenv('CSIRTG_TOKEN', None)

TIMEOUT = os.getenv('CSIRTG_TIMEOUT', 30)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

HEADERS = {
    'User-Agent': 'csirtgsdk-py/' + VERSION,
    'x-api-key': TOKEN,
    'Content-Type': 'application/json',
    'Accept-Encoding': 'deflate',
    'Accept': 'application/vnd.csirtg.v' + API_VERSION
}

CACHE_MAX_SIZE = os.getenv('CSIRTG_CACHE_MAX_SIZE', 1024)
CACHE_TTL = os.getenv('CSIRTG_CACHE_TTL', 3600)

SESSION = requests_retry_session()
SESSION.headers = HEADERS
