from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

from ctlml_commons.entity.execution_type import ExecutionType
from ctlml_commons.entity.price import Price
from ctlml_commons.entity.state import State
from ctlml_commons.entity.time_in_force import TimeInForce
from ctlml_commons.util.date_utils import convert_dates, datetime_to_str
from ctlml_commons.util.num_utils import convert_floats

ERROR_DETAIL_KEY: str = "detail"


class OrderType(Enum):
    LIMIT = auto()
    MARKET = auto()

    @staticmethod
    def to_enum(value: str) -> Optional[OrderType]:
        v: str = value.upper().replace(" ", "-").replace("-", "_")
        return OrderType[v]

    def value(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class OptionalOrder:
    order: Optional[Order] = None
    detail: Optional[str] = None

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = self.__dict__

        if self.order is not None:
            data['order'] = self.order.serialize()

        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> OptionalOrder:
        return OptionalOrder(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if ERROR_DETAIL_KEY not in input_data:
            return {"order": Order.deserialize(input_data=deepcopy(input_data))}

        return deepcopy(input_data)


@dataclass(frozen=True)
class OrderExecution:
    id: str
    price: float
    quantity: float
    settlement_date: datetime
    timestamp: datetime

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = self.__dict__

        data["settlement_date"] = datetime_to_str(self.settlement_date)
        data["timestamp"] = datetime_to_str(self.timestamp)

        return data

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> OrderExecution:
        return OrderExecution(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data = convert_floats(data, ["price", "quantity"])
        data = convert_dates(data, "settlement_date", "timestamp")

        return data


@dataclass(frozen=True)
class Order:
    id: str
    ref_id: str
    url: str
    account: str
    position: str
    cancel: str
    instrument: str
    cumulative_quantity: float
    state: State
    type: OrderType
    side: ExecutionType
    time_in_force: TimeInForce
    trigger: str  # TODO: enum
    price: Price
    quantity: float
    created_at: datetime
    updated_at: datetime
    last_transaction_at: datetime
    executions: List[OrderExecution]
    extended_hours: bool
    override_dtbp_checks: bool
    override_day_trade_checks: bool
    stop_triggered_at: datetime
    last_trail_price: float
    last_trail_price_updated_at: datetime
    average_price: Optional[float] = None
    fees: Optional[float] = None
    stop_price: Optional[Price] = None
    reject_reason: Optional[str] = None
    response_category: Optional[str] = None
    dollar_based_amount: Optional[Price] = None
    drip_dividend_id: Optional[str] = None
    total_notional: Optional[Price] = None
    executed_notional: Optional[Price] = None
    investment_schedule_id: Optional[str] = None
    details: Optional[str] = None
    is_ipo_access_order: Optional[bool] = None
    ipo_access_lower_collared_price: Optional[Any] = None
    ipo_access_upper_collared_price: Optional[Any] = None
    ipo_access_upper_price: Optional[Any] = None
    ipo_access_lower_price: Optional[Any] = None
    ipo_access_cancellation_reason: Optional[Any] = None

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = self.__dict__

        print(f"data: {type(self.time_in_force)} --- {self.time_in_force} - {data['time_in_force']}")
        data["state"] = self.state.value()
        data["time_in_force"] = self.time_in_force.value()
        data["side"] = self.side.value()
        data["type"] = self.type.value()
        data["executions"] = [e.serialize() for e in self.executions]
        data["last_transaction_at"] = datetime_to_str(self.last_transaction_at)
        data["stop_triggered_at"] = datetime_to_str(self.stop_triggered_at)
        data["last_trail_price_updated_at"] = datetime_to_str(self.last_trail_price_updated_at)
        data["created_at"] = datetime_to_str(self.created_at)
        data["updated_at"] = datetime_to_str(self.updated_at)

        return data

    def execution_stats(self) -> Tuple[float, float, float]:
        quantity = sum([e.quantity for e in self.executions])
        total_price = sum([e.quantity * e.price for e in self.executions])
        per_share_price = total_price / quantity

        return quantity, total_price, per_share_price

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> Order:
        return Order(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data["state"] = State.to_enum(data["state"])
        data["time_in_force"] = TimeInForce.to_enum(data["time_in_force"])
        data["side"] = ExecutionType.to_enum(data["side"])
        data["type"] = OrderType.to_enum(data["type"])
        data["executions"] = [OrderExecution.deserialize(input_data=e) for e in data["executions"]]

        consolidate_price_data(
            data, ["price", "stop_price", "dollar_based_amount", "total_notional", "executed_notional"]
        )

        data = convert_floats(
            data, ["cumulative_quantity", "quantity", "average_price", "fees", "stop_price", "last_trail_price"]
        )
        data = convert_dates(data, "last_transaction_at", "stop_triggered_at", "last_trail_price_updated_at")

        return data


def consolidate_price_data(input_data: Dict[str, Any], keys: List[str]) -> None:
    """In some cases, the price is a primitive, in others its in a single item list so handle both cases

    Args:
        input_data: input data
        keys: price keys
    """
    for key in keys:
        if key not in input_data:
            #  Skip missing key
            print(f"Skipping missing key: {key}")
        elif type(input_data[key]) in [str, float]:
            input_data[key] = Price.deserialize(input_data={"amount": input_data[key]})
        else:
            input_data[key] = Price.deserialize(input_data[key]) if input_data[key] is not None else None
