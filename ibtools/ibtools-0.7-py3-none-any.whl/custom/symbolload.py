import datetime
import pandas as pd
from ib_insync import Stock, ScannerSubscription, TagValue
import ibtools as ibt


class Instrument:
    def __init__(self, contract):
        self.contract = contract
        self.symbol = contract.symbol

    def __str__(self):
        return 'Instrument: '+str(self.symbol) + '\n' + str(self.contract)


def instrumentsFromScan():
    sub = ScannerSubscription(instrument='STK',
                              locationCode='STK.NASDAQ',
                              numberOfRows=50,
                              aboveVolume=100000,
                              scanCode='TOP_PERC_GAIN')

    priceAbove = TagValue("priceAbove", "5")
    priceBelow = TagValue("priceBelow", "30")
    optVolumeAbove = TagValue("optVolumeAbove", "1000")
    avgVolumeAbove = TagValue("avgVolumeAbove", "10000")
    optVolumePCRatioAbove = TagValue("optVolumePCRatioAbove", "1")
    tags = [priceAbove,
            priceBelow,
            optVolumeAbove,
            optVolumeAbove,
            avgVolumeAbove,
            optVolumePCRatioAbove]

    scanData = ibt.app.reqScannerData(sub, tags, tags)
    return instrumentsFromScanResult(scanData)


def toDateFromString(dateStr):
    return datetime.datetime.strptime(dateStr, "%Y%m%d").date()


def symbolDescriptionFromFile(filePath):
    df = pd.read_csv(filePath, sep=',', names=[
                     "Cat", "Symbol", "Exchange", "Currency"])
    dfFiltered = df[df['Cat'] == 'SYM']
    del dfFiltered['Cat']
    return dfFiltered


def createContract(symbolParam, exchangeParam):
    return Stock(symbol=symbolParam, exchange=exchangeParam)


def createContracts(symbolsDescription):
    return [createContract(row['Symbol'], row['Exchange'])
            for _, row in symbolsDescription.iterrows()]


def createInstruments(filePath):
    symbolsDescription = symbolDescriptionFromFile(filePath)
    contracts = createContracts(symbolsDescription)
    return {contract.symbol: Instrument(contract) for contract in contracts}


def instrumentsFromScanResult(scanData):
    contracts = [scanData.contractDetails.contract for scanData in scanData]
    return {contract.symbol: Instrument(contract) for contract in contracts}


def validChainsFromInstruments(instruments, chainsFetcher):
    chainsForInstrument = {instrument: chainsFetcher(instrument) for instrument in instruments.values()}
    return {instrument: chains for instrument, chains in chainsForInstrument.items() if len(chains) > 0}
