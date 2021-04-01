import pandas as pd
import ibtools as ibt
from tools import today, toDate
from ib_insync import Future
from IPython.utils import io


def contractsFromNow(symbol, endDate):
    expirationCandidates = allFridays(today(), toDate(endDate))
    contractCandidates = [Future(symbol=symbol,
                                 lastTradeDateOrContractMonth=expirationCandidate)
                          for expirationCandidate in expirationCandidates]
    with io.capture_output():  # Trying to suppress Error 200 from TWS
        return ibt.app.qualifyContracts(*contractCandidates)


def allFridays(beginDate, endDate):
    return pd.date_range(beginDate,
                         endDate,
                         freq='W-FRI').strftime(ibt.twsDateFormat).tolist()
