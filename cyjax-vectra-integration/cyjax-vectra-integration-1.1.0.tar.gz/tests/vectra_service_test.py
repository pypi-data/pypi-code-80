import unittest
from datetime import timedelta, datetime
from unittest.mock import Mock

from src.configuration import LAST_SYNC_TIMESTAMP
from src.vectra_service import VectraService
from tests import create_mock_configuration


class VectraServiceTest(unittest.TestCase):

    def setUp(self):
        self.configuration = create_mock_configuration()

    def test_send_indicators(self):
        # Mock save timestamp to config file
        self.configuration.save_last_sync_timestamp = Mock()

        # Set last run timestamp
        expected_last_timestamp = (datetime.now() - timedelta(days=1)).astimezone()
        self.configuration.config[LAST_SYNC_TIMESTAMP] = expected_last_timestamp

        vectra_service = VectraService(self.configuration)
        indicators_client = Mock()
        indicators_client.list.return_value = []
        vectra_service.indicators_client = indicators_client
        vectra_service.send_indicators()

        indicators_client.list.assert_called_with(
            since=expected_last_timestamp, type='Hostname,Domain,URL,IPv4,IPv6')

    def test_get_default_last_timestamp(self):
        vectra_service = VectraService(self.configuration)

        assert vectra_service.last_run_timestamp is None

        last_timestamp = vectra_service._get_last_timestamp()
        expected_last_timestamp = datetime.now().astimezone() - timedelta(days=3)

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectra_service.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()

    def test_get_last_timestamp_from_memory(self):
        expected_last_timestamp = (datetime.now() - timedelta(days=2)).astimezone()

        vectra_service = VectraService(self.configuration)

        assert vectra_service.last_run_timestamp is None

        vectra_service.last_run_timestamp = expected_last_timestamp

        assert vectra_service.last_run_timestamp is not None

        last_timestamp = vectra_service._get_last_timestamp()

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectra_service.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()

    def test_get_last_timestamp_from_configuration(self):
        expected_last_timestamp = (datetime.now() - timedelta(days=1)).astimezone()
        self.configuration.config[LAST_SYNC_TIMESTAMP] = expected_last_timestamp

        vectra_service = VectraService(self.configuration)

        assert vectra_service.last_run_timestamp is None

        last_timestamp = vectra_service._get_last_timestamp()

        assert expected_last_timestamp.replace(microsecond=0).isoformat() == \
               last_timestamp.replace(microsecond=0).isoformat()

        assert vectra_service.last_run_timestamp.replace(microsecond=0).isoformat() == \
               expected_last_timestamp.replace(microsecond=0).isoformat()
