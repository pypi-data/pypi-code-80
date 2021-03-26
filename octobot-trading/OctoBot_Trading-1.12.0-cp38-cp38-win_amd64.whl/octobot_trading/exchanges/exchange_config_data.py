#  Drakkar-Software OctoBot-Trading
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import octobot_commons.symbol_util as symbol_util
import octobot_commons.time_frame_manager as time_frame_manager
import octobot_commons.constants as constants
import octobot_commons.logging as logging

import octobot_trading.util as util


class ExchangeConfig(util.Initializable):
    def __init__(self, exchange_manager):
        super().__init__()
        self._logger = logging.get_logger(self.__class__.__name__)

        self.exchange_manager = exchange_manager
        self.config = exchange_manager.config

        # dict of exchange supported pairs by enabled currencies from self.config
        self.traded_cryptocurrencies = {}
        # list of exchange supported enabled pairs from self.config
        self.traded_symbol_pairs = []
        # list of exchange supported pairs from self.config
        self.all_config_symbol_pairs = []
        # list of exchange supported time frames
        self.traded_time_frames = []
        # list of time frames to be used for real-time purposes (short time frames)
        self.real_time_time_frames = []

    async def initialize_impl(self):
        pass

    def set_config_traded_pairs(self):  # TODO
        self._set_config_traded_pairs()

    def set_config_time_frame(self):  # TODO
        self._set_config_time_frame()

    def get_shortest_time_frame(self):
        return self.traded_time_frames[-1]

    async def handle_symbol_update(self, exchange: str, exchange_id: str, crypto_currency: str, symbols: list) -> tuple:
        try:
            return self._add_tradable_symbols(crypto_currency, symbols)
        except Exception as e:
            self._logger.exception(e, True, f"Fail to handle symbol update : {e}")

    async def handle_time_frame_update(self, exchange: str, exchange_id: str, time_frames: list) -> list:
        try:
            return self._add_tradable_time_frames(time_frames)
        except Exception as e:
            self._logger.exception(e, True, f"Fail to handle time frame update : {e}")

    def _set_config_traded_pairs(self):
        self.traded_cryptocurrencies = {}
        traded_symbol_pairs_set = set()
        existing_pairs = set()
        for cryptocurrency in self.config[constants.CONFIG_CRYPTO_CURRENCIES]:
            if self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_PAIRS]:
                is_enabled = util.is_currency_enabled(self.config, cryptocurrency, True)
                if self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_PAIRS] != \
                        constants.CONFIG_SYMBOLS_WILDCARD:
                    self._populate_non_wildcard_pairs(cryptocurrency, existing_pairs, is_enabled)
                else:
                    self._populate_wildcard_pairs(cryptocurrency, existing_pairs, is_enabled)
                # add to global traded pairs
                if is_enabled:
                    if not self.traded_cryptocurrencies[cryptocurrency]:
                        self._logger.error(
                            f"{self.exchange_manager.exchange_name} is not supporting any {cryptocurrency} trading pair"
                            f" from the current configuration.")
                    traded_symbol_pairs_set = traded_symbol_pairs_set.union(
                        self.traded_cryptocurrencies[cryptocurrency]
                    )
            else:
                self._logger.error(f"Current configuration for {cryptocurrency} is not including any trading pair, "
                                   f"this asset can't be traded and related orders won't be loaded. "
                                   f"OctoBot requires at least one trading pair in configuration to handle an asset. "
                                   f"You can add trading pair(s) for each asset in the configuration section.")
        self.traded_symbol_pairs = list(traded_symbol_pairs_set)
        self.all_config_symbol_pairs = list(existing_pairs)

    def _populate_non_wildcard_pairs(self, cryptocurrency, existing_pairs, is_enabled):
        if self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_PAIRS] != \
                constants.CONFIG_SYMBOLS_WILDCARD:
            currency_pairs = []
            for symbol in self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][
                constants.CONFIG_CRYPTO_PAIRS]:
                if self.exchange_manager.symbol_exists(symbol):
                    if is_enabled:
                        currency_pairs.append(symbol)
                    # also add disabled pairs to existing pairs since they still exist on exchange
                    existing_pairs.add(symbol)
                elif is_enabled:
                    self._logger.error(f"{self.exchange_manager.exchange_name} is not supporting the "
                                       f"{symbol} trading pair.")
            if is_enabled:
                self.traded_cryptocurrencies[cryptocurrency] = currency_pairs

    def _populate_wildcard_pairs(self, cryptocurrency, existing_pairs, is_enabled):
        wildcard_pairs_list = self._create_wildcard_symbol_list(self.config[constants.CONFIG_CRYPTO_CURRENCIES]
                                              [cryptocurrency][constants.CONFIG_CRYPTO_QUOTE])

        # additional pairs
        if constants.CONFIG_CRYPTO_ADD in self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency]:
            wildcard_pairs_list += self._add_tradable_symbols_from_config(cryptocurrency,
                                                                          wildcard_pairs_list)

        if is_enabled:
            self.traded_cryptocurrencies[cryptocurrency] = wildcard_pairs_list

        # also add disabled pairs to existing pairs since they still exist on exchange
        existing_pairs.update(wildcard_pairs_list)

    def _set_config_time_frame(self):
        for time_frame in time_frame_manager.get_config_time_frame(self.config):
            if self.exchange_manager.time_frame_exists(time_frame.value):
                self.traded_time_frames.append(time_frame)
        if not self.exchange_manager.is_backtesting or not self.traded_time_frames:
            # add shortest time frame for realtime evaluators or if no time frame at all has
            # been registered in backtesting
            client_shortest_time_frame = time_frame_manager.find_min_time_frame(
                self.exchange_manager.client_time_frames,
                constants.MIN_EVAL_TIME_FRAME)
            self.real_time_time_frames.append(client_shortest_time_frame)
        self.traded_time_frames = list(set().union(self.traded_time_frames, self.real_time_time_frames))
        self.traded_time_frames = time_frame_manager.sort_time_frames(self.traded_time_frames, reverse=True)

    @staticmethod
    def _is_tradable_with_cryptocurrency(symbol, cryptocurrency):
        return symbol if symbol_util.split_symbol(symbol)[1] == cryptocurrency else None

    def _add_tradable_symbols_from_config(self, cryptocurrency, filtered_symbols):
        return [
            symbol
            for symbol in self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_ADD]
            if self.exchange_manager.symbol_exists(symbol) and symbol not in filtered_symbols
        ]

    def _create_wildcard_symbol_list(self, cryptocurrency):
        return [s for s in [ExchangeConfig._is_tradable_with_cryptocurrency(symbol, cryptocurrency)
                            for symbol in self.exchange_manager.client_symbols]
                if s is not None]

    def _add_tradable_symbols(self, cryptocurrency, symbols):
        if cryptocurrency not in self.config[constants.CONFIG_CRYPTO_CURRENCIES]:
            # TODO use exchange config
            self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency] = {}
            self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_PAIRS] = symbols
            return cryptocurrency, symbols

        # TODO manage wildcard
        symbols_to_add = [s for s in symbols
                          if self.exchange_manager.symbol_exists(s)
                          and s not in self.config[constants.CONFIG_CRYPTO_CURRENCIES]
                          [cryptocurrency][constants.CONFIG_CRYPTO_PAIRS]]

        # TODO use exchange config
        self.config[constants.CONFIG_CRYPTO_CURRENCIES][cryptocurrency][constants.CONFIG_CRYPTO_PAIRS] += symbols_to_add

        return None, symbols_to_add

    def _add_tradable_time_frames(self, time_frames):
        # TODO use exchange config
        time_frames_to_add = [tf for tf in time_frames
                              if self.exchange_manager.time_frame_exists(tf)
                              and tf not in self.config[constants.CONFIG_TIME_FRAME]]
        return time_frames_to_add
