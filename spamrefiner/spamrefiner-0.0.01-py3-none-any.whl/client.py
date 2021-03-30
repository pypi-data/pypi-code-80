from typing import Union
import requests


class Client:
    def __init__(self, token: str, *, host: str = 'http://api.spamrefiner.org') -> None:
        self._host = host
        self._token = token

    def get_flag(self, user_id: int) -> Union[bool]:
        try:
            r = requests.get(f"{self._host}/find?id={user_id}&token={self._token}")
            req = r.json()
            if req.get("error"):
                if req["error"] == "invalid token":
                    flag_info = "Please check your API Token, It seems to be incorrect!"
                else:
                    flag_info = req["error"]
            elif req.get("reason"):
                flag_info = True
            else:
                flag_info = False
            return flag_info
        except:
            error = "Unknown Error Occured"
            return error

    def get_flag_reason(self, user_id: int) -> Union[bool]:
        try:
            r = requests.get(f"{self._host}/find?id={user_id}&token={self._token}")
            req = r.json()
            if req.get("error"):
                if req["error"] == "invalid token":
                    flag_info = "Please check your API Token, It seems to be incorrect!"
                else:
                    flag_info = req["error"]
            elif req.get("reason"):
                flag_info = req["reason"]
            else:
                flag_info = "This User is not flagged!"
            return flag_info
        except:
            error = "Unknown Error Occured"
            return error

