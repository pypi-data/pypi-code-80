from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from ctlml_commons.util.date_utils import convert_dates
from ctlml_commons.util.num_utils import convert_floats


@dataclass(frozen=True)
class Portfolio:
    url: str
    account: str
    start_date: datetime
    market_value: float
    equity: float
    extended_hours_market_value: float
    extended_hours_equity: float
    extended_hours_portfolio_equity: float
    last_core_market_value: float
    last_core_equity: float
    last_core_portfolio_equity: float
    excess_margin: float
    excess_maintenance: float
    excess_margin_with_uncleared_deposits: float
    excess_maintenance_with_uncleared_deposits: float
    equity_previous_close: float
    portfolio_equity_previous_close: float
    adjusted_equity_previous_close: float
    adjusted_portfolio_equity_previous_close: float
    withdrawable_amount: float
    unwithdrawable_deposits: float
    unwithdrawable_grants: float

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Portfolio:
        return Portfolio(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data = convert_floats(
            data,
            [
                "market_value",
                "equity",
                "extended_hours_market_value",
                "extended_hours_equity",
                "extended_hours_portfolio_equity",
                "last_core_market_value",
                "last_core_equity",
                "last_core_portfolio_equity",
                "excess_margin",
                "excess_maintenance",
                "excess_margin_with_uncleared_deposits",
                "excess_maintenance_with_uncleared_deposits",
                "equity_previous_close",
                "portfolio_equity_previous_close",
                "adjusted_equity_previous_close",
                "adjusted_portfolio_equity_previous_close",
                "withdrawable_amount",
                "unwithdrawable_deposits",
                "unwithdrawable_grants",
            ],
        )
        data = convert_dates(data, "start_date")

        return data
