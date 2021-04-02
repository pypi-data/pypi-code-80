import datetime
import typing

import praw

from . import model, proxy


class StockData:
    symbol: str
    data_proxy: proxy.DataProxy

    def __init__(
        self, symbol: str, data_proxy: typing.Type[proxy.DataProxy], *args, **kwargs
    ):
        self.symbol = symbol
        self.data_proxy = data_proxy(symbol, *args, **kwargs)

    def get_info(self) -> model.StockInformation:
        return self.data_proxy.get_info()

    def get_last_price(self) -> float:
        return self.data_proxy.get_last_price()

    def get_stock_price_history(
        self, interval: datetime.timedelta, period: datetime.timedelta
    ) -> typing.List[model.StockHistoryDatum]:
        return self.data_proxy.get_stock_price_history(interval, period)

    def get_option_chain(self, date: datetime.datetime) -> model.OptionChain:
        return self.data_proxy.get_option_chain(date)

    def get_next_option_chain(self) -> model.OptionChain:
        return self.data_proxy.get_option_chain(date=None)

    def get_full_option_chain(
        self
    ) -> typing.Dict[datetime.datetime, model.OptionChain]:
        return self.data_proxy.get_full_option_chain()

    def get_reddit_threads(
        self, subreddits: typing.List, time_filter: str = "day", sort: str = "hot"
    ) -> typing.List[praw.models.Submission]:
        return self.data_proxy.get_reddit_threads(subreddits, time_filter, sort)
