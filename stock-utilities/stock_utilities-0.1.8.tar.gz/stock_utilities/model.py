import dataclasses
import datetime
import enum
import math
import typing

import numpy as np
import scipy.stats as scipy_stats

import py_vollib.ref_python.black.greeks.analytical as vollib_a

from . import exceptions


class OptionType(enum.Enum):
    UNDEFINED = 0
    CALL = 1
    PUT = 2


class CorrelationHistoryDatum(typing.NamedTuple):
    time: datetime.datetime
    value: float


class StockHistoryDatum(typing.NamedTuple):
    time: datetime.datetime
    symbol: str
    currency: str
    open_value: float
    close_value: float
    high: float
    low: float
    volume: float
    dividends: float
    stock_splits: float


@dataclasses.dataclass
class StockInformation:
    time: int
    symbol: typing.Optional[str] = None
    logo_url: typing.Optional[str] = None
    long_name: typing.Optional[str] = None
    average_volume_10_days: typing.Optional[float] = None
    average_volume: typing.Optional[float] = None
    market_cap: typing.Optional[float] = None
    float_shares: typing.Optional[float] = None
    short_ratio: typing.Optional[float] = None
    short_percent_float: typing.Optional[float] = None
    shares_short: typing.Optional[float] = None
    shares_short_previous_month_date: typing.Optional[float] = None
    shares_short_prior_month: typing.Optional[float] = None
    shares_percent_shares_out: typing.Optional[float] = None
    shares_outstanding: typing.Optional[float] = None
    shares_implied_outstanding: typing.Optional[float] = None
    shares_held_percent_insiders: typing.Optional[float] = None
    shares_held_percent_institution: typing.Optional[float] = None


class OptionChainDatum(typing.NamedTuple):
    type: OptionType
    strike: float
    current_stock_price: float
    bid: float
    open_interest: float
    currency: str
    last_price: float
    implied_volatility: float
    option_date: datetime.datetime
    last_trade_date: datetime.datetime

    def delta(self, risk: float = 0.0) -> float:
        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()
        expire = (self.option_date - datetime.datetime.now()).total_seconds() / (
            365 * 24 * 60.0
        )

        if self.type == OptionType.CALL:
            return vollib_a.delta(
                "c",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )
        else:
            return vollib_a.delta(
                "p",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )

    def gamma(self, risk: float = 0) -> float:
        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()
        expire = (self.option_date - datetime.datetime.now()).total_seconds() / (
            365 * 24 * 60.0
        )

        if self.type == OptionType.CALL:
            return vollib_a.gamma(
                "c",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )
        else:
            return vollib_a.gamma(
                "p",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )

    def tetha(self, risk: float = 0) -> float:
        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()
        expire = (self.option_date - datetime.datetime.now()).total_seconds() / (
            365 * 24 * 60.0
        )

        if self.type == OptionType.CALL:
            return vollib_a.tetha(
                "c",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )
        else:
            return vollib_a.tetha(
                "p",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )

    def rho(self, risk: float = 0) -> float:
        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()
        expire = (self.option_date - datetime.datetime.now()).total_seconds() / (
            365 * 24 * 60.0
        )

        if self.type == OptionType.CALL:
            return vollib_a.rho(
                "c",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )
        else:
            return vollib_a.rho(
                "p",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )

    def vega(self, risk: float = 0) -> float:
        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()
        expire = (self.option_date - datetime.datetime.now()).total_seconds() / (
            365 * 24 * 60.0
        )

        if self.type == OptionType.CALL:
            return vollib_a.vega(
                "c",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )
        else:
            return vollib_a.vega(
                "p",
                self.current_stock_price,
                self.strike,
                expire,
                risk,
                self.implied_volatility,
            )

    def payoff(self, contract_size: int = 100, position: int = 1) -> float:
        # negative position means short

        if self.type == OptionType.UNDEFINED:
            raise exceptions.OptionTypeIsUndefined()

        if self.type == OptionType.CALL:
            if position > 0:
                return (
                    (max(0, self.current_stock_price - self.strike) - self.last_price)
                    * contract_size
                    * position
                )
            else:
                return (
                    (self.last_price - max(0, self.current_stock_price - self.strike))
                    * contract_size
                    * position
                )
        else:
            if position > 0:
                return (
                    (max(0, self.strike - self.current_stock_price) - self.last_price)
                    * contract_size
                    * position
                )
            else:
                return (
                    (self.last_price - max(0, self.strike - self.current_stock_price))
                    * contract_size
                    * position
                )


class OptionChain(typing.NamedTuple):
    calls: typing.List[OptionChainDatum]
    puts: typing.List[OptionChainDatum]
