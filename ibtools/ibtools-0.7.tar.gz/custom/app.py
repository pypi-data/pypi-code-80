from ib_insync import IB
import ibtools as ibt


def connect():
    ibs = IB()
    ibt.app = ibs
    ibt.marketDataObservable = ibt.MarketDataStream(ibs)
    ibt.cacheFilePath = 'cache/'
    conn = ibs.connect(port=7497, clientId=1)
    if conn:
        print('Connection established')
    else:
        print('Connection failed!')
    return ibs
