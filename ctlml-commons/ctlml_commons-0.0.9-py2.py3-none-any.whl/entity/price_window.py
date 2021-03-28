from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class PriceWindow:
    floor: float
    ceiling: float

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> PriceWindow:
        return PriceWindow(**input_data)
