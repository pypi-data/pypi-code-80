from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict

from ctlml_commons.entity.focus.focus import Focus
from ctlml_commons.entity.range_window import RangeWindow


@dataclass(frozen=True)
class PriceFocus(Focus):
    """Price up/down based investment strategy."""

    """Per share price window range"""
    per_share_price_window: RangeWindow

    """Total lot profit/loss threshold"""
    total_threshold: float

    """Number of periods to consider for purchase decisions"""
    num_periods: int

    """If should sell at the end of day"""
    sell_at_end_of_day: bool

    def serialize(self) -> Dict[str, Any]:
        data = deepcopy(self.__dict__)
        data["per_share_price_window"] = self.per_share_price_window.serialize()
        data["focus_type"] = self.__class__.__name__
        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> PriceFocus:
        data = deepcopy(input_data)

        del data["focus_type"]
        data["per_share_price_window"] = RangeWindow.deserialize(data["per_share_price_window"])

        return cls(**data)
