from .defaults import GUEST_UID, GUEST_KEY
from .logger import logger


class ChaiAuth:
    def __init__(self, uid: str, key: str):
        self._uid = uid
        self._key = key
        self.accessed = False

    @property
    def is_guest(self):
        return self._uid == GUEST_UID

    @property
    def uid(self) -> str:
        if not self.accessed and self.is_guest:
            logger.warning("Using guest credentials. To be able to redeploy and monitor your Chat AIs, "
                           "run chai_py.set_auth with your uid and key from https://chai.ml/dev/")
            self.accessed = True
        return self._uid

    @property
    def key(self) -> str:
        return self._key


auth = ChaiAuth(uid=GUEST_UID, key=GUEST_KEY)


def set_auth(uid: str, key: str):
    """Sets package-wide developer authentication.

    :param uid: Developer Unique Identifier.
    :param key: Developer key.
    :return:
    """
    global auth
    auth = ChaiAuth(uid=uid, key=key)


def get_auth():
    return auth
