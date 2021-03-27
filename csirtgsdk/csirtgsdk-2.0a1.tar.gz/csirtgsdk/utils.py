import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

RETRIES = os.getenv('CSIRTGSDK_RETRIES', 5)
BACKOFF = os.getenv('CSIRTGSDK_BACKOFF', 0.5)

ALLOWED = frozenset({'GET', 'OPTIONS', 'POST', 'HEAD'})


def requests_retry_session(retries=RETRIES, backoff_factor=BACKOFF,
                           status_forcelist=(429, 504),
                           session=None):

    session = session or requests.Session()
    retry = Retry(total=int(retries), method_whitelist=ALLOWED,
                  read=int(retries), connect=int(retries),
                  backoff_factor=float(backoff_factor),
                  status_forcelist=status_forcelist)

    adapter = HTTPAdapter(max_retries=retry, pool_connections=128,
                          pool_maxsize=128)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
