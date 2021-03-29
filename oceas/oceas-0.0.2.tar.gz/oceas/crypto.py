import requests 

def all_crypto():
    all_crypto = requests.get('https://api.binance.com/api/v3/ticker/24hr')
    all_crypto = all_crypto.json()
    print(all_crypto)

def BTC_USDT():
    BTC_USDT = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
    BTC_USDT = BTC_USDT.json()
    print(BTC_USDT)


