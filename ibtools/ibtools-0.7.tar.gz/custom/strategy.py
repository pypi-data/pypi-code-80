import random
from ordermgmt import *
from optiondata import *
import ibtools as ibt
from ib_insync import MarketOrder
import pandas as pd
from ibtools import requestMarketData, cancelMarketData
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None


class Leg:

    def __init__(self, option, direction, ratio=1):
        self.option = option
        self.direction = direction
        self.ratio = ratio
        self.conId = option.conId
        self.exchange = option.exchange


class MaxPain:

    def __init__(self, name, chains):
        self.name = name
        self.chains = chains
        self.underlying = next(iter(chains.values())).underlying
        self.expirations = list(self.chains.keys())

    def start(self, onEvalReady):
        self.onEvalReady = onEvalReady
        self.undMarketData = requestMarketData(self.underlying)
        self.marketDataForChains = ibt.OptionChainsMarketData(self.chains)

        firstKey = next(iter(self.marketDataForChains.keys()))
        self.marketDataForChains[firstKey].subscribe(self.__onMarketDataSubscribed)

    def stop(self):
        self.undMarketData = cancelMarketData(self.underlying)
        self.marketDataForChains.unsubscribe()
        print(f"Strategy {self.name} is now stopped.")

    def __onMarketDataSubscribed(self, data):
        self.expirations = list(self.chains.keys())
        marketDataForFirstChain = self.marketDataForChains[self.expirations[0]]

        self.callDF = dataFrameFromChainMarketData(marketDataForFirstChain.calls)
        self.putDF = dataFrameFromChainMarketData(marketDataForFirstChain.puts)
        self.__evaluate()

    def __evaluate(self):
        maxPainStrikeIndex = self.__maxPainIndexForChain()
        maxPainStrike = self.callDF.iloc[maxPainStrikeIndex]['strike']

        if maxPainStrike >= self.undMarketData.ask:
            self.__contractForMaxPain(self.callDF, maxPainStrike)
        else:
            self.__contractForMaxPain(self.putDF, maxPainStrike)

    def __contractForMaxPain(self, df, maxPainStrike):
        self.contract = self.chains[self.expirations[0]].calls[maxPainStrike].option
        #data = df[df['strike'] == maxPainStrike]
        #spread = data.iloc[0]['spread']
        #ask = data.iloc[0]['ask']
        data = rowForStrike(df, maxPainStrike)
        spread = valueForRow(data, 'spread')
        ask = valueForRow(data, 'ask')
        spreadRel = spread/ask
        print('Strategy', self.name, 'for', self.underlying.symbol,
              'evaluated maxPain at', maxPainStrike, 'with confidence', spreadRel)
        self.onEvalReady(self, spreadRel)

    def __totalLossAtStrike(self, strikeAtExpiration):
        lossForCalls = self.__lossAtStrikeForItmOptions(strikeAtExpiration, 'C', self.callDF)
        lossForPuts = self.__lossAtStrikeForItmOptions(strikeAtExpiration, 'P', self.putDF)
        #itmCalls = self.__inTheMoneyStrikes(self.callDF, 'C', strikeAtExpiration)
        #itmCalls["CEloss"] = (strikeAtExpiration - itmCalls['strike'])*itmCalls["openInterest"]

        #itmPuts = self.__inTheMoneyStrikes(self.putDF, 'P', strikeAtExpiration)
        #itmPuts["PEloss"] = (itmPuts['strike'] - strikeAtExpiration)*itmPuts["openInterest"]
        #total_loss = itmCalls["CEloss"].sum() + itmPuts["PEloss"].sum()
        total_loss = lossForCalls.sum() + lossForPuts.sum()

        return total_loss

    def __lossAtStrikeForItmOptions(self, strikeAtExpiration, right, df):
        itmOptions = self.__inTheMoneyStrikes(df, right, strikeAtExpiration)
        return (strikeAtExpiration - itmOptions['strike'])*itmOptions["openInterest"]

    def __maxPainIndexForChain(self):
        strikes = self.callDF['strike']
        losses = [self.__totalLossAtStrike(strike)/1000000 for strike in strikes]

        #plt.plot(strikes, losses)
        #plt.ylabel('Total loss in rs (Millon)')
        # plt.show()

        maxPainStrikeIndex = losses.index(min(losses))
        return maxPainStrikeIndex

    def __inTheMoneyStrikes(self, df, right, undPrice):
        if right == 'C':
            return df.loc[df['strike'] < undPrice]
        return df.loc[df['strike'] > undPrice]

    def startTrade(self):
        order = MarketOrder('BUY', 1, transmit=False)
        # order.smartComboRoutingParams = []
        # order.smartComboRoutingParams.append(TagValue("NonGuaranteed", "1"))
        # contract = Contract(conId=)

        orderInformation = OrderInformation(self.contract, order)
        trade = placeOrder(orderInformation)
        trade.filledEvent += self.__onFillUpdate

    def __onFillUpdate(self, trade):
        print('Trade update {trade}')

    def __str__(self):
        return 'Strategy: '+self.name
