from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, Optional

from ctlml_commons.entity.crypto.balance import Balance
from ctlml_commons.util.date_utils import date_parse


@dataclass(frozen=True)
class TransactionDestination:
    address: str
    address_url: str
    currency: str
    resource: str
    address_info: Optional[TransactionDestinationInfo] = None

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[TransactionDestination]:
        if data is None:
            return data
        return cls(**cls.clean(data))

    @classmethod
    def clean(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if "address_info" in data:
            data["address_info"] = TransactionDestinationInfo.deserialize(data["address_info"])

        return data


@dataclass(frozen=True)
class TransactionDestinationInfo:
    address: str

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[TransactionDestinationInfo]:
        if data is None:
            return data
        return cls(**data)


@dataclass(frozen=True)
class TransactionSource:
    id: Optional[str] = None
    resource: Optional[str] = None
    resource_path: Optional[str] = None
    currency: Optional[str] = None

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[TransactionSource]:
        if data is None:
            return None
        return cls(**data)


class TransactionHealth(Enum):
    POSITIVE = auto()

    @staticmethod
    def to_enum(value: str) -> TransactionHealth:
        t: str = value.upper()
        return TransactionHealth[t]

    def value(self) -> str:
        return self.name.lower()

    def serialize(self) -> str:
        return self.value()


@dataclass(frozen=True)
class TransactionDetails:
    header: str
    health: TransactionHealth
    subtitle: str
    title: str
    payment_method_name: Optional[str] = None

    def serialize(self) -> Dict[str, Any]:
        data = deepcopy(self.__dict__)

        data["health"] = self.health.serialize()

        return data

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[TransactionDetails]:
        if data is None:
            return data
        return cls(**cls.clean(data))

    @classmethod
    def clean(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["health"] = TransactionHealth.to_enum(data["health"])

        return data


class TransactionType(Enum):
    BUY = auto()
    EXCHANGE_DEPOSIT = auto()
    FIAT_DEPOSIT = auto()
    INFLATION_REWARD = auto()
    INTEREST = auto()
    PRO_WITHDRAWAL = auto()
    SEND = auto()
    STAKING_REWARD = auto()
    TRADE = auto()

    @staticmethod
    def to_enum(value: str) -> TransactionType:
        t: str = value.upper()
        return TransactionType[t]

    def value(self) -> str:
        return self.name.lower()

    def serialize(self) -> str:
        return self.value()


class TransactionResource(Enum):
    TRANSACTION = auto()

    @staticmethod
    def to_enum(value: str) -> TransactionResource:
        t: str = value.upper()
        return TransactionResource[t]

    def value(self) -> str:
        return self.name.lower()

    def serialize(self) -> str:
        return self.value()


class TransactionStatus(Enum):
    COMPLETED = auto()
    CONFIRMED = auto()
    OFF_BLOCKCHAIN = auto()
    UNKNOWN = auto()

    @staticmethod
    def to_enum(value: str) -> TransactionStatus:
        if value is None:
            return TransactionStatus.UNKNOWN

        t: str = value.upper()
        return TransactionStatus[t]

    def value(self) -> str:
        return self.name.lower()

    def serialize(self) -> str:
        return self.value()


@dataclass(frozen=True)
class Network:
    status: TransactionStatus
    status_description: str
    hash: Optional[str] = None
    transaction_url: Optional[str] = None
    confirmations: Optional[str] = None
    transaction_amount: Optional[Balance] = None
    transaction_fee: Optional[Balance] = None

    def serialize(self) -> Dict[str, Any]:
        data = deepcopy(self.__dict__)

        data["status"] = self.status.serialize()

        return data

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[Network]:
        if data is None:
            return data
        return cls(**cls.clean(data))

    @classmethod
    def clean(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        if data is not None:
            data["status"] = TransactionStatus.to_enum(data["status"])

            for field in ["transaction_amount", "transaction_fee"]:
                if field in data:
                    data[field] = Balance.deserialize(data[field])

        return data


@dataclass(frozen=True)
class Transaction:
    id: str
    amount: Balance
    native_amount: Balance
    type: TransactionType
    status: TransactionStatus
    resource: TransactionResource
    details: TransactionDetails
    created_at: datetime
    updated_at: datetime
    resource_path: str
    description: Optional[str] = None
    instant_exchange: Optional[bool] = False
    off_chain_status: Optional[TransactionStatus] = None
    network: Optional[Network] = None
    source: Optional[TransactionSource] = None
    buy: Optional[TransactionSource] = None
    trade: Optional[TransactionSource] = None
    fiat_deposit: Optional[TransactionSource] = None
    application: Optional[TransactionSource] = None
    to: Optional[TransactionDestination] = None
    idem: Optional[str] = None

    def serialize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = deepcopy(self.__dict__)

        data["type"] = self.type.serialize()
        data["status"] = self.status.serialize()
        data["resource"] = self.resource.serialize()
        data["details"] = self.details.serialize()

        if "off_chain_status" in data and data["off_chain_status"] is not None:
            data["off_chain_status"] = self.off_chain_status.serialize()

        if "network" in data and data["network"] is not None:
            data["network"] = self.network.serialize()

        return data

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> Optional[Transaction]:
        if data is None:
            return data
        return cls(**cls.clean(data))

    @classmethod
    def clean(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["amount"] = Balance.deserialize(data["amount"])
        data["native_amount"] = Balance.deserialize(data["native_amount"])
        data["details"] = TransactionDetails.deserialize(data["details"])

        data["type"] = TransactionType.to_enum(data["type"])
        data["status"] = TransactionStatus.to_enum(data["status"])

        if "off_chain_status" in data:
            data["off_chain_status"] = TransactionStatus.to_enum(data["off_chain_status"])

        data["resource"] = TransactionResource.to_enum(data["resource"])

        for source in ["application", "buy", "fiat_deposit", "from", "trade"]:
            if source in data:
                data[source] = TransactionSource.deserialize(data[source])

                if source in ["from"]:
                    del data[source]

        data["created_at"] = date_parse(data["created_at"])
        data["updated_at"] = date_parse(data["updated_at"])

        if "network" in data:
            data["network"] = Network.deserialize(data["network"])
        return data
