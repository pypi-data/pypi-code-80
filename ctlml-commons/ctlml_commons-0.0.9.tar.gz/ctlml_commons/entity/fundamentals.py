from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict

from ctlml_commons.util.num_utils import convert_floats


@dataclass(frozen=True)
class Fundamentals:
    open: float
    high: float
    low: float
    volume: float
    market_date: str
    average_volume_2_weeks: float
    average_volume: float
    high_52_weeks: float
    dividend_yield: float
    float: float
    low_52_weeks: float
    market_cap: float
    pb_ratio: float
    pe_ratio: float
    shares_outstanding: float
    description: str
    instrument: str
    ceo: str
    headquarters_city: str
    headquarters_state: str
    sector: str
    industry: str
    num_employees: int
    year_founded: int
    symbol: str

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Fundamentals:
        return Fundamentals(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data = convert_floats(
            data,
            [
                "open",
                "high",
                "low",
                "volume",
                "average_volume_2_weeks",
                "average_volume",
                "high_52_weeks",
                "low_52_weeks",
                "market_cap",
                "shares_outstanding",
            ],
        )
        data = convert_floats(data, ["dividend_yield", "float", "pb_ratio", "pe_ratio"], 0.00)

        return data
