from datetime import datetime
from enum import Enum, auto


class SpamRefinerType:
    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.__dict__}>'

    def __repr__(self) -> str:
        return self.__str__()


class Flag(SpamRefinerType):
    user_id: int
    flagged: str
    reason: str

    def __init__(self,
                 flagged: str,
                 reason: str,
                 user_id: int,
                 **kwargs) -> None:
        self.user_id = user_id
        self.flagged = flagged
        self.reason = reason