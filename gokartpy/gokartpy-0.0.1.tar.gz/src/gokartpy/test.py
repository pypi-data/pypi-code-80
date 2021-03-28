from abc import abstractmethod, ABC
from dataclasses import dataclass


@dataclass
class TestGokartpy(ABC):
    x: float
    y: float
    z: float

    @abstractmethod
    def print(self):
        ...
