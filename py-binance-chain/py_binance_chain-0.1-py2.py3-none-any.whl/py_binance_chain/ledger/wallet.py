from typing import Optional

from py_binance_chain.environment import BinanceEnvironment
from py_binance_chain.wallet import BaseWallet
from py_binance_chain.ledger.client import LedgerApp


class LedgerWallet(BaseWallet):

    def __init__(self, app: LedgerApp, env: Optional[BinanceEnvironment] = None):
        super().__init__(env)
        self._app = app
        pk_address = self._app.get_address()
        self._public_key = pk_address['pk']
        self._address = pk_address['address']

    def sign_message(self, msg_bytes):
        return self._app.sign(msg_bytes)
