import typing

import pandas

from . import model, stock_data


def correlation(symbol_one: str, symbol_two: str):
    pass


def correlation_history(
    history_one: typing.List[model.StockHistoryDatum],
    history_two: typing.List[model.StockHistoryDatum],
    length=5,
) -> typing.List[model.CorrelationHistoryDatum]:

    d1 = pandas.DataFrame(data=history_one)
    d2 = pandas.DataFrame(data=history_two)

    d1 = d1.set_index("time")
    d2 = d2.set_index("time")

    merge = pandas.merge(d1, d2, on="time", suffixes=["_1", "_2"])

    df = pandas.DataFrame(merge, columns=["close_value_1", "close_value_2"])
    data = df["close_value_1"].rolling(length).corr(other=df["close_value_2"]).dropna()
    data.columns = ["value"]

    return [
        model.CorrelationHistoryDatum(time=v[1], value=v[0])
        for v in zip(data, data.index)
    ]
