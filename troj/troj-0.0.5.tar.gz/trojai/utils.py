import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests import Session

retry_strategy = Retry(
    total=4,
    backoff_factor=1,
    status_forcelist=[403, 429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT",
                      "POST", "DELETE", "OPTIONS", "TRACE"],
)
retry_adapter = HTTPAdapter(max_retries=retry_strategy)
requests_retry = Session()
requests_retry.mount("https://", retry_adapter)
requests_retry.mount("http://", retry_adapter)
tempdir_ttl_days = 1

# MAX_FRAMES_PER_BATCH = 1000
# MAX_CHUNK_SIZE = int(pow(2, 23))  # 8 MiB

def assert_valid_name(name: str):
    is_valid = re.match(r"^[A-Za-z0-9_]+$", name)
    if not is_valid:
        raise Exception(
            f"'{name}' must only contain alphanumeric and underscore characters."
        )


# TODO:
# Different exceptions thrown so far:
# (no header) Exception: HTTP Error received: Forbidden: 403 | Not authenticated
# (bad id_token) Exception: HTTP Error received: Forbidden: 403 | JWK invalid
# If resp.json().detail is 'Not authenticated'
# Direct them to check their id_token or use id_token and refresh_token to generate new id_token?


def raise_resp_exception_error(resp):
    if not resp.ok:
        message = None
        try:
            r_body = resp.json()
            message = r_body.get("message") or r_body.get("msg")
        except:
            # If we failed for whatever reason (parsing body, etc.)
            # Just return the code
            if resp.status_code == 500:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)}"
                )
            else:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)} | {resp.json()['detail']}"
                )
                # return resp.json()['detail']
        if message:
            raise Exception(f"Error: {message}")
        else:
            # Don't really need this if, can be removed and keep what's in the else
            if resp.status_code == 500:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)}"
                )
            else:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)} | {resp.json()['detail']}"
                )
                # return resp.json()['detail']
