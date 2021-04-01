import pandas as pd
from enum import Enum


class OptionType(Enum):
    CALL = 0
    PUT = 1


def dataFrameFromChainMarketData(chainMarketDataByStrike):
    chainMarketData = chainMarketDataByStrike.values()
    right = next(iter(chainMarketData)).right
    marketDataOfChainOptions = [optionMarketData.marketData
                                for optionMarketData in chainMarketData]

    data = {'strike': list(chainMarketDataByStrike.keys()),
            'bid': [marketData.bid for marketData in marketDataOfChainOptions],
            'bidSize': [marketData.bidSize for marketData in marketDataOfChainOptions],
            'ask': [marketData.ask for marketData in marketDataOfChainOptions],
            'askSize': [marketData.askSize for marketData in marketDataOfChainOptions],
            'spread': [marketData.ask-marketData.bid for marketData in marketDataOfChainOptions],
            'openInterest': _getOpenInterest(marketDataOfChainOptions, right),
            'delta': [marketData.modelGreeks.delta for marketData in marketDataOfChainOptions],
            'gamma': [marketData.modelGreeks.gamma for marketData in marketDataOfChainOptions],
            'vega': [marketData.modelGreeks.vega for marketData in marketDataOfChainOptions],
            'theta': [marketData.modelGreeks.theta for marketData in marketDataOfChainOptions],
            'undPrice': [marketData.modelGreeks.undPrice for marketData in marketDataOfChainOptions]}

    return _roundDataframe(pd.DataFrame(data))


def rowForStrike(df, strike):
    return df.loc[df['strike'] == strike]


def valueForRow(row, attribute):
    return row.iloc[0][attribute]


def valueForStrike(df, strike, attribute):
    return valueForRow(rowForStrike(df, strike), attribute)


def _getOpenInterest(marketDataOfChainOptions, right):
    if right == 'C':
        return [marketData.callOpenInterest
                for marketData in marketDataOfChainOptions]
    return [marketData.putOpenInterest
            for marketData in marketDataOfChainOptions]


def _roundDataframe(df):
    return df.round({'strike': 1,
                     'bid': 2,
                     'ask': 2,
                     'spread': 2,
                     'undPrice': 2,
                     'delta': 4,
                     'gamma': 4,
                     'vega': 4,
                     'theta': 4,
                     'undPrice': 2})
