from datetime import datetime
from enum import Enum, auto
from typing import Optional


class SpamWatchType:
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.__dict__}>'

    def __repr__(self) -> str:
        return self.__str__()


class Ban(SpamWatchType):
    user_id: int
    flagged: str
    reason: str

    def __init__(self,
                 user_id: int,
                 flagged: str,
                 reason: str,
                 **kwargs) -> None:
        self.user_id = user_id
        self.flagged = flagged
        self.reason = reason