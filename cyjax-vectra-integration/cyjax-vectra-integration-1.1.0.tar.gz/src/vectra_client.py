"""The module contains the Vectra REST client."""

import logging
import logging.config

import requests


# pylint: disable=too-few-public-methods
class VectraClient:
    """The VectraClient class provides the client to perform REST API requests to Vectra."""
    BASE_URI = 'https://%s/api/v2.1/threatFeeds'

    def __init__(self, vectra_fqdn: str, vectra_key: str, vectra_threat_feeds, ssl_verification: bool = True):
        self.logger = logging.getLogger('cyjax-vectra')
        self.base_url = self.BASE_URI % (vectra_fqdn,)
        self.vectra_threat_feeds = vectra_threat_feeds
        self.headers = {'Authorization': 'token %s' % vectra_key}
        self.ssl_verification = ssl_verification

    def send_daily_indicators(self, file_path):
        """
        Sends daily indicators.
        @param file_path: :param file_path: The STIX file path.
        """
        self._send(self.base_url + '/' + self.vectra_threat_feeds[0], file_path)

    def send_weekly_indicators(self, file_path):
        """
        Sends weekly indicators.
        @param file_path: :param file_path: The STIX file path.
        """
        self._send(self.base_url + '/' + self.vectra_threat_feeds[1], file_path)

    def _send(self, url, file_path):
        """
        Sends the indicator file to Vectra.
        :param url: The URL.
        :param file_path: The STIX file path.
        :raises ResponseErrorException: Whether the request fails.
        :raises ApiKeyNotFoundException: Whether the API key is not provided.
        :raises UnauthorizedException: Whether the API key is not authorized to perform the request.
        :raises TooManyRequestsException: Whether the API key exceeds the rate limit.
        """
        files = [('file', (file_path, open(file_path, 'rb'), 'text/xml'))]
        response = requests.request('POST', url, headers=self.headers, files=files,
                                    verify=self.ssl_verification)

        if response.status_code != 200:
            self.logger.error("Error sending API request to Vectra code:%s, message:%s", response.status_code,
                              response.text)
        else:
            self.logger.info("Successfully sent API request to Vectra: %s", response.text)

        return response

    def health(self):
        """
        Checks whether vectra push service can talk to vectra endpoint.
        """
        return requests.request('GET', self.base_url + '/' + self.vectra_threat_feeds[0], headers=self.headers,
                                verify=self.ssl_verification)
