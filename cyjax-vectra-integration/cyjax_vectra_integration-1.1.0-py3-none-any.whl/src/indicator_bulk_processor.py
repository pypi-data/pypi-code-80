"""
The IndicatorBulkProcessor class manages the bulk process to send indicator to Vectra.
It creates a .xml that contains the indicators to be sent.
It sends indicators in batches of MAX_INDICATORS_PER_FILE.
"""

import logging
import os
import time
from os import path

from cybox.core import Object
from cybox.core.observable import Observable
from cybox.objects.address_object import Address
from cybox.objects.domain_name_object import DomainName
from cybox.objects.hostname_object import Hostname
from cybox.objects.uri_object import URI
from stix.core import STIXPackage, STIXHeader
from stix.indicator import Indicator, IndicatorType

from src.configuration import Configuration
from src.indicator_enum import URL_TYPE, IPV4_TYPE, IPV6_TYPE, DOMAIN_TYPE, HOSTNAME_TYPE
from src.vectra_client import VectraClient


class IndicatorBulkProcessor:
    """Processes indicators."""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, configuration: Configuration):
        self.count = 0
        self.open = False
        self.configuration = configuration
        self.logger = logging.getLogger('cyjax-vectra')
        self.vectra_client = VectraClient(
            configuration.get_vectra_fqdn(),
            configuration.get_vectra_api_key(),
            configuration.get_vectra_threat_feed_ids(),
            configuration.get_vectra_ssl_verification()
        )
        self.daily_stix_package = None
        self.weekly_stix_package = None
        self.daily_stix_file_path = configuration.get_daily_stix_file_path()
        self.weekly_stix_file_path = configuration.get_weekly_stix_file_path()

    def _clean_up_old_stix_files(self):
        """
        Removes old STIX files.
        """
        current_timestamp = time.time()
        for stix_file in os.listdir(self.configuration.get_config_path()):
            stix_file_path = os.path.join(self.configuration.get_config_path(), stix_file)
            if stix_file[0:5] == 'stix-' and stix_file[-4:] == '.xml' and os.stat(
                    stix_file_path).st_mtime < current_timestamp - 7 * 86400:
                self.logger.info("Removing STIX file %s", stix_file_path)
                os.remove(stix_file_path)

    def _create_stix_package(self):
        """
        Creates the STIX package. If the daily and weekly STIX files exist, use those
        as starting point.
        """
        self.daily_stix_package = STIXPackage.from_xml(self.daily_stix_file_path) if path.exists(
            self.daily_stix_file_path) else STIXPackage(stix_header=STIXHeader())
        self.weekly_stix_package = STIXPackage.from_xml(self.weekly_stix_file_path) if path.exists(
            self.weekly_stix_file_path) else STIXPackage(stix_header=STIXHeader())

    def add(self, indicator: dict) -> None:
        """
        Adds an indicator to the bulk processor
        :param indicator: The indicator.
        """
        if not self.open:
            self._clean_up_old_stix_files()
            self._create_stix_package()
            self.open = True

        self.logger.debug("Adding indicator: %s", indicator['value'])
        self.count += 1
        self.daily_stix_package.add_indicator(self.parse_indicator_to_stix(indicator))
        self.weekly_stix_package.add_indicator(self.parse_indicator_to_stix(indicator))

    def close(self) -> None:
        """
        Closes the bulk processor.
        """
        if self.count > 0:
            self._send()

    def _send(self) -> None:
        """
        Sends the indicators and saves them to a STIX file.
        """
        self.logger.info("Found new %s indicators", self.count)
        # Write the STIX package to files
        with open(self.daily_stix_file_path, 'wb') as stix_file:
            stix_file.write(self.daily_stix_package.to_xml())
        with open(self.weekly_stix_file_path, 'wb') as stix_file:
            stix_file.write(self.weekly_stix_package.to_xml())
        self.vectra_client.send_daily_indicators(self.daily_stix_file_path)
        self.vectra_client.send_weekly_indicators(self.weekly_stix_file_path)

    @staticmethod
    def parse_indicator_to_stix(indicator: dict) -> Indicator:
        """
        Parses an indicator to stix format.
        @param indicator: The indicator.
        @return The indicator.
        """

        # Create a CyboX Object
        indicator_type = None
        cybox_object = None
        if indicator['type'] == URL_TYPE:
            indicator_type = IndicatorType.TERM_URL_WATCHLIST
            cybox_object = URI(indicator['value'])
            cybox_object.type_ = URI.TYPE_URL
        elif indicator['type'] == IPV4_TYPE or indicator['type'] == IPV6_TYPE:
            indicator_type = IndicatorType.TERM_IP_WATCHLIST
            cybox_object = Address(indicator['value'])
            cybox_object.category = Address.CAT_IPV4 if indicator['type'] == IPV4_TYPE else Address.CAT_IPV6
        elif indicator['type'] == DOMAIN_TYPE:
            indicator_type = IndicatorType.TERM_DOMAIN_WATCHLIST
            cybox_object = DomainName()
            cybox_object.value = indicator['value']
        elif indicator['type'] == HOSTNAME_TYPE:
            indicator_type = IndicatorType.TERM_HOST_CHARACTERISTICS
            cybox_object = Hostname()
            cybox_object.hostname_value = indicator['value']

        stix_indicator = Indicator()
        stix_indicator.title = 'Indicator of compromise'
        if indicator_type:
            stix_indicator.add_indicator_type(indicator_type)
        if indicator['description']:
            stix_indicator.add_description(indicator['description'])

        observable = Observable(id_=indicator['uuid'])
        observable.object_ = Object(properties=cybox_object)

        stix_indicator.add_observable(observable)

        return stix_indicator
