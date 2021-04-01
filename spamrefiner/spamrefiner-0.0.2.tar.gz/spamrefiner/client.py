from typing import Union
from .types import Flag
import requests


class Client:
    def __init__(self, token: str, *, host: str = 'http://api.spamrefiner.org') -> None:
        self._host = host
        self._token = token

    def get_flag(self, user_id: int) -> Union[Flag, bool]:
        try:
            data = requests.get(f"{self._host}/find?id={user_id}&token={self._token}")
            req = data.json()
            if req.get("error"):
                if req["error"] == "invalid token":
                    error = "Please check your API Token, It seems to be incorrect!"
                else:
                    error = req["error"]
                return error
            elif req.get("reason"):
                return Flag(**req)
            else:
                return "User not flagged"
        except:
            error = "Unknown Error Occured"
            return error
