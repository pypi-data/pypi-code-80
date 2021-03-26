# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.base.exchange import Exchange
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound


class coindcx(Exchange):

    def describe(self):
        return self.deep_extend(super(coindcx, self).describe(), {
            'id': 'coindcx',
            'name': 'CoinDCX',
            'countries': ['IN'],  # india
            'urls': {
                'api': {
                    'general': 'https://api.coindcx.com',
                    'public': 'https://public.coindcx.com',
                    'private': 'https://api.coindcx.com',
                },
                'www': 'https://coindcx.com/',
                'doc': 'https://coindcx-official.github.io/rest-api/',
                'fees': 'https://coindcx.com/fees',
            },
            'version': 'v1',
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'token': False,
            },
            'api': {
                'general': {
                    'get': [
                        'exchange/ticker',
                        'exchange/v1/markets',
                        'exchange/v1/markets_details',
                    ],
                },
                'public': {
                    'get': [
                        'market_data/trade_history',
                        'market_data/orderbook',
                        'market_data/candles',
                    ],
                },
                'private': {
                    'post': [
                        'exchange/v1/users/balances',
                        'exchange/v1/orders/create',
                        'exchange/v1/orders/status',
                        'exchange/v1/orders/active_orders',
                        'exchange/v1/orders/trade_history',
                        'exchange/v1/orders/cancel',
                        'exchange/v1/orders/cancel_all',
                    ],
                },
            },
            'has': {
                'fetchTicker': 'emulated',
                'fetchTickers': True,
                'fetchTrades': True,
                'fetchOrderBook': True,
                'fetchOHLCV': True,
                'fetchBalance': True,
                'fetchOrder': True,
                'fetchOpenOrders': True,
                'createLimitOrder': True,
                'createMarketOrder': True,
                'createOrder': True,
                'cancelOrder': True,
                'cancelAllOrders': True,
                'editOrder': False,
            },
            'timeframes': {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '8h': '8h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1M',
            },
            'fees': {
                'byExchange': {
                    'I': 0.001,  # coindcx
                    'HB': 0.002,  # hitbtc
                    'H': 0.002,  # huobi
                    'B': 0.001,  # binance
                    'BM': None,  # bitmex
                },
            },
            'timeout': 10000,
            'rateLimit': 2000,
            'exceptions': {
                'Invalid Request.': BadRequest,  # Yeah, with a dot at the end.
                'Invalid credentials': PermissionDenied,
                'Insufficient funds': InsufficientFunds,
                'Quantity too low': InvalidOrder,
                'Order not found': OrderNotFound,
            },
        })

    def fetch_markets(self, params={}):
        # answer example https://coindcx-official.github.io/rest-api/?javascript#markets-details
        details = self.generalGetExchangeV1MarketsDetails(params)
        result = []
        for i in range(0, len(details)):
            market = details[i]
            id = self.safe_string(market, 'symbol')
            quoteId = self.safe_string(market, 'base_currency_short_name')
            quote = self.safe_currency_code(quoteId)
            baseId = self.safe_string(market, 'target_currency_short_name')
            base = self.safe_currency_code(baseId)
            symbol = base + '/' + quote
            exchangeCode = self.safe_string(market, 'ecode')
            feeRate = self.safe_float(self.fees['byExchange'], exchangeCode)
            active = False
            if market['status'] == 'active':
                active = True
            precision = {
                'amount': self.safe_integer(market, 'target_currency_precision'),
                'price': self.safe_integer(market, 'base_currency_precision'),
            }
            limits = {
                'amount': {
                    'min': self.safe_float(market, 'min_quantity'),
                    'max': self.safe_float(market, 'max_quantity'),
                },
                'price': {
                    'min': self.safe_float(market, 'min_price'),
                    'max': self.safe_float(market, 'max_price'),
                },
            }
            result.append({
                'id': id,
                'symbol': symbol,
                'base': base,
                'quote': quote,
                'baseId': baseId,
                'quoteId': quoteId,
                'active': active,
                'taker': feeRate,
                'maker': feeRate,
                'precision': precision,
                'limits': limits,
                'info': market,
            })
        return result

    def fetch_tickers(self, symbols=None, params={}):
        self.load_markets()
        response = self.generalGetExchangeTicker(params)
        result = {}
        for i in range(0, len(response)):
            ticker = self.parse_ticker(response[i])
            # I found out that sometimes it returns tickers that aren't in the markets, so we should no add self to results
            if ticker is None:
                continue
            symbol = ticker['symbol']
            result[symbol] = ticker
        return result

    def fetch_ticker(self, symbol, params={}):
        self.load_markets()
        response = self.generalGetExchangeTicker(params)
        market = self.market(symbol)
        result = {}
        for i in range(0, len(response)):
            if response[i]['market'] != market['id']:
                continue
            result = self.parse_ticker(response[i])
            break
        return result

    def parse_ticker(self, ticker):
        # Sometimes the bid and ask are plain wrong, not trustworthy
        timestamp = self.safe_timestamp(ticker, 'timestamp')
        tickersMarket = self.safe_string(ticker, 'market')
        if not (tickersMarket in self.markets_by_id):
            return None
        market = self.markets_by_id[tickersMarket]
        last = self.safe_float(ticker, 'last_price')
        percentage = self.safe_float(ticker, 'change_24_hour')
        open = None
        change = None
        average = None
        if last is not None and percentage is not None:
            open = last / (1 + percentage / 100)
            change = last - open
            average = (open + last) / 2
        return {
            'symbol': market['symbol'],
            'info': ticker,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_float(ticker, 'high'),
            'low': self.safe_float(ticker, 'low'),
            'bid': self.safe_float(ticker, 'bid'),
            'bidVolume': None,
            'ask': self.safe_float(ticker, 'ask'),
            'askVolume': None,
            'vwap': None,
            'open': open,
            'close': last,
            'last': last,
            'previousClose': None,
            'change': change,
            'percentage': percentage,
            'average': average,
            'baseVolume': self.safe_float(ticker, 'volume'),
            'quoteVolume': None,
        }

    def fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=500, params={}):
        # https://coindcx-official.github.io/rest-api/?shell#candles
        self.load_markets()
        market = self.market(symbol)
        coindcxPair = self.get_pair_from_info(market)
        coindcxTimeframe = self.timeframes[timeframe]
        if coindcxTimeframe is None:
            raise ExchangeError(self.id + ' has no "' + timeframe + '" timeframe')
        if limit is None:
            limit = 500
        request = {
            'pair': coindcxPair,
            'interval': coindcxTimeframe,
            'limit': limit,
        }
        response = self.publicGetMarketDataCandles(self.extend(request, params))
        return self.parse_ohlcvs(response, market, timeframe, since, limit)

    def parse_ohlcv(self, ohlcv, market=None, timeframe='1m', since=None, limit=None):
        return [
            self.safe_integer(ohlcv, 'time'),
            self.safe_float(ohlcv, 'open'),
            self.safe_float(ohlcv, 'high'),
            self.safe_float(ohlcv, 'low'),
            self.safe_float(ohlcv, 'close'),
            self.safe_float(ohlcv, 'volume'),
        ]

    def fetch_trades(self, symbol, since=None, limit=30, params={}):
        # https://coindcx-official.github.io/rest-api/?shell#trades
        self.load_markets()
        market = self.market(symbol)
        coindcxPair = self.get_pair_from_info(market)
        if limit is None:
            limit = 30
        request = {
            'pair': coindcxPair,
            'limit': limit,
        }
        response = self.publicGetMarketDataTradeHistory(self.extend(request, params))
        return self.parse_trades(response, market, since, limit)

    def fetch_my_trades(self, symbol=None, since=None, limit=500, params={}):
        # https://coindcx-official.github.io/rest-api/?javascript#account-trade-history
        self.load_markets()
        if limit is None:
            limit = 500
        request = {
            'timestamp': self.milliseconds(),
            'limit': limit,
        }
        response = self.privatePostExchangeV1OrdersTradeHistory(self.extend(request, params))
        return self.parse_trades(response, None, since, limit)

    def parse_trade(self, trade, market=None):
        timestamp = self.safe_integer_2(trade, 'T', 'timestamp')
        symbol = None
        if market is None:
            marketId = self.safe_string_2(trade, 's', 'symbol')
            market = self.safe_value(self.markets_by_id, marketId)
        if market is not None:
            symbol = market['symbol']
        side = self.safe_string(trade, 'side')
        takerOrMaker = None
        if 'm' in trade:  # m stands for whether the buyer is market maker or not
            takerSide = 'sell' if trade['m'] else 'buy'
            if side is None:
                takerOrMaker = 'taker'
                side = takerSide
            else:
                takerOrMaker = 'taker' if (side == takerSide) else 'maker'
        price = self.safe_float_2(trade, 'p', 'price')
        amount = self.safe_float_2(trade, 'q', 'quantity')
        fee = None
        feeCost = self.safe_float(trade, 'fee_amount')
        if feeCost is not None and market is not None:
            fee = {
                'cost': feeCost,
                'currency': market['quote'],
                'rate': self.safe_float(self.fees['byExchange'], self.safeString(trade, 'ecode')),  # taker and maker are equal
            }
        return {
            'id': self.safe_string(trade, 'id'),
            'info': trade,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'symbol': symbol,
            'order': self.safe_string(trade, 'order_id'),
            'type': None,
            'takerOrMaker': takerOrMaker,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': price * amount,
            'fee': fee,
        }

    def fetch_order_book(self, symbol, limit=None, params={}):
        # May return corrupted ob, like fetchTicker does with bid / ask
        # https://coindcx-official.github.io/rest-api/?shell#order-book
        self.load_markets()
        market = self.market(symbol)
        coindcxPair = self.get_pair_from_info(market)
        request = {
            'pair': coindcxPair,
        }
        response = self.publicGetMarketDataOrderbook(self.extend(request, params))
        # parseOrderBook in python won't you do parseBidsAsks on non-array bidasks, hence it must be done here
        response['bids'] = self.parse_order_book_branch(self.safe_value(response, 'bids', {}))
        response['asks'] = self.parse_order_book_branch(self.safe_value(response, 'asks', {}))
        return self.parse_order_book(response)

    def parse_order_book_branch(self, bidasks, priceKey=None, amountKey=None):
        priceKeys = list(bidasks.keys())
        parsedData = []
        for i in range(0, len(priceKeys)):
            amountKey = priceKeys[i]
            price = float(amountKey)
            amount = float(bidasks[amountKey])
            parsedData.append([price, amount])
        return parsedData

    def fetch_balance(self, params={}):
        # https://coindcx-official.github.io/rest-api/?javascript#get-balances
        self.load_markets()
        request = {
            'timestamp': self.milliseconds(),
        }
        response = self.privatePostExchangeV1UsersBalances(self.extend(request, params))
        result = {'info': response}
        for i in range(0, len(response)):
            balance = response[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            if not (code in result):
                account = self.account()
                account['free'] = self.safe_float(balance, 'balance')
                account['used'] = self.safe_float(balance, 'locked_balance')
                account['total'] = self.sum(account['free'], account['used'])
                result[code] = account
        return self.parse_balance(result)

    def fetch_order(self, id, symbol=None, params={}):
        # https://coindcx-official.github.io/rest-api/?javascript#account-trade-history
        self.load_markets()
        request = {
            'id': id,
        }
        response = self.privatePostExchangeV1OrdersStatus(self.extend(request, params))
        return self.parse_order(response)

    def fetch_open_orders(self, symbol=None, since=None, limit=None, params={}):
        self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOpenOrders requires a symbol argument')
        market = self.market(symbol)
        request = {
            'market': self.safe_value(market, 'id'),
            'timestamp': self.milliseconds(),
        }
        response = self.privatePostExchangeV1OrdersActiveOrders(self.extend(request, params))
        orders = self.safe_value(response, 'orders', [])
        return self.parse_orders(orders, market, since, limit)

    def create_order(self, symbol, type, side, amount, price=None, params={}):
        # https://coindcx-official.github.io/rest-api/?javascript#new-order
        self.load_markets()
        market = self.market(symbol)
        marketInfo = self.safe_value(market, 'info')
        orderType = 'limit_order'
        if type == 'market':
            orderType = 'market_order'
        request = {
            'market': self.safe_value(marketInfo, 'symbol'),
            'total_quantity': amount,
            'side': side,
            'order_type': orderType,
            'timestamp': self.milliseconds(),
        }
        if orderType == 'limit_order':
            request['price_per_unit'] = price
        response = self.privatePostExchangeV1OrdersCreate(self.extend(request, params))
        orders = self.safe_value(response, 'orders', [])
        return self.parse_order(orders[0], market)

    def cancel_order(self, id, symbol=None, params={}):
        self.load_markets()
        request = {
            'id': id,
            'timestamp': self.milliseconds(),
        }
        return self.privatePostExchangeV1OrdersCancel(self.extend(request, params))

    def cancel_all_orders(self, symbol=None, params={}):
        self.load_markets()
        market = self.market(symbol)
        request = {
            'market': self.safe_value(market, 'id'),
            'timestamp': self.milliseconds(),
        }
        return self.privatePostExchangeV1OrdersCancelAll(self.extend(request, params))

    def parse_order_status(self, status):
        statuses = {
            'init': 'open',
            'open': 'open',
            'partially_filled': 'open',
            'filled': 'closed',
            'rejected': 'rejected',
            'canceled': 'canceled',
            'partially_cancelled': 'canceled',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order, market=None):
        id = self.safe_string(order, 'id')
        timestamp = self.parse_date(self.safe_string(order, 'created_at'))
        if timestamp is None:
            timestamp = self.safe_integer(order, 'created_at')
        lastTradeTimestamp = self.parse_date(self.safe_string(order, 'updated_at'))
        if lastTradeTimestamp is None:
            lastTradeTimestamp = self.safe_integer(order, 'updated_at')
        orderStatus = self.safe_string(order, 'status')
        status = self.parse_order_status(orderStatus)
        marketId = self.safe_string(market, 'symbol')
        if market is None:
            market = self.safe_value(self.markets_by_id, marketId)
        amount = self.safe_float(order, 'total_quantity')
        remaining = self.safe_float(order, 'remaining_quantity')
        average = self.safe_float(order, 'avg_price')
        filled = None
        cost = None
        if amount is not None and remaining is not None:
            filled = amount - remaining
            if average is not None:
                cost = filled * average
        if average == 0:
            average = None
        symbol = None
        quoteSymbol = None
        fee = None
        if market is not None:
            symbol = self.safe_string(market, 'symbol')
            quoteSymbol = self.safe_string(market, 'quote')
            if quoteSymbol is not None:
                fee = {
                    'currency': quoteSymbol,
                    'rate': self.safe_float(order, 'fee'),
                    'cost': self.safe_float(order, 'fee_amount'),
                }
        type = self.safe_string(order, 'order_type')
        if type == 'market_order':
            type = 'market'
        elif type == 'limit_order':
            type = 'limit'
        return {
            'id': id,
            'datetime': self.iso8601(timestamp),
            'timestamp': timestamp,
            'lastTradeTimestamp': lastTradeTimestamp,
            'status': status,
            'symbol': symbol,
            'type': type,
            'side': self.safe_string(order, 'side'),
            'price': self.safe_float_2(order, 'price', 'price_per_unit'),
            'amount': amount,
            'filled': filled,
            'remaining': remaining,
            'cost': cost,
            'average': average,
            'trades': None,
            'fee': fee,
            'info': order,
        }

    def get_pair_from_info(self, market):
        marketInfo = self.safe_value(market, 'info')
        coindcxPair = self.safe_string(marketInfo, 'pair')
        if coindcxPair is None:
            raise ExchangeError(self.id + ' has no pair(look at market\'s info) value for ' + market['symbol'])
        return coindcxPair

    def sign(self, path, api='public', method='GET', params={}, headers=None, body=None):
        base = self.urls['api'][api]
        request = '/' + self.implode_params(path, params)
        url = base + request
        query = self.omit(params, self.extract_params(path))
        if method == 'GET':
            if query:
                suffix = '?' + self.urlencode(query)
                url += suffix
        if api == 'private':
            self.check_required_credentials()
            body = self.json(query)
            signature = self.hmac(self.encode(body), self.encode(self.secret))
            headers = {
                'Content-Type': 'application/json',
                'X-AUTH-APIKEY': self.apiKey,
                'X-AUTH-SIGNATURE': signature,
            }
        return {'url': url, 'method': method, 'body': body, 'headers': headers}

    def handle_errors(self, code, reason, url, method, headers, body, response, requestHeaders, requestBody):
        if not response:
            return
        if code >= 400:
            feedback = self.id + ' ' + body
            message = self.safe_string(response, 'message')
            if message is not None:
                self.throw_exactly_matched_exception(self.exceptions, message, feedback)
            self.throw_exactly_matched_exception(self.httpExceptions, str(code), feedback)
            raise ExchangeError(feedback)  # unknown message
