from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ctlml_commons.util.date_utils import convert_dates
from ctlml_commons.util.num_utils import convert_floats


@dataclass(frozen=True)
class Quote:
    ask_price: float
    ask_size: int
    bid_price: float
    bid_size: int
    last_trade_price: float
    last_extended_hours_trade_price: float
    previous_close: float
    adjusted_previous_close: float
    previous_close_date: datetime
    symbol: str
    trading_halted: bool
    has_traded: bool
    last_trade_price_source: str
    instrument: str
    updated_at: datetime

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Quote:
        return Quote(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data = convert_floats(
            data,
            [
                "ask_price",
                "bid_price",
                "last_trade_price",
                "last_extended_hours_trade_price",
                "previous_close",
                "adjusted_previous_close",
            ],
        )

        data = convert_dates(data, "previous_close_date")

        return data
