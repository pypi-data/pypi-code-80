from enum import Enum
from ib_insync import Bag, ComboLeg
import ibtools as ibt


class OrderDirection(Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderInformation():

    def __init__(self, contract, order):
        self.contract = contract
        self.order = order

        #self.legs = legs
        #self.comboLegs = [comboLegFromLeg(leg) for leg in legs]
        #firstOption = legs[0].option
        #self.symbol = firstOption.symbol
        #self.exchange = firstOption.exchange
        #self.currency = firstOption.currency


def placeOrder(orderInformation):
    trade = ibt.app.placeOrder(orderInformation.contract, orderInformation.order)
    print('Placed trade: ', trade)
    return trade


def createComboContract(orderInformation):
    return Bag(symbol=orderInformation.symbol,
               exchange=orderInformation.exchange,
               comboLegs=orderInformation.comboLegs,
               currency=orderInformation.currency)


def comboLegFromLeg(leg):
    return ComboLeg(leg.conId,
                    leg.ratio,
                    str(leg.direction.value),
                    leg.exchange)
