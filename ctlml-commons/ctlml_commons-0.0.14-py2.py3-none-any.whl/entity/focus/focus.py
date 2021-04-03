from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any, Dict


class Focus(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """Serialize a investment focus.

        Returns:
            serialized investment focus
        """
