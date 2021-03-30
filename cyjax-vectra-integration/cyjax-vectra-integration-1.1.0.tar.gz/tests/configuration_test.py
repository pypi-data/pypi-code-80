import unittest

from src.configuration import CYJAX_API_KEY, VECTRA_FQDN, VECTRA_DAILY_THREAT_FEED_ID, \
    VECTRA_WEEKLY_THREAT_FEED_ID, VECTRA_API_KEY, InvalidConfigurationException, \
    CONFIG_FILE_PATH
from tests import create_mock_configuration


class ConfigurationTest(unittest.TestCase):

    def setUp(self):
        self.configuration = create_mock_configuration()

    def test_validate_with_no_cyjax_key(self):
        del self.configuration.config[CYJAX_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_cyjax_key(self):
        self.configuration.config[CYJAX_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Cyjax API key cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_fqdn(self):
        del self.configuration.config[VECTRA_FQDN]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra FQDN cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_fqdn(self):
        self.configuration.config[VECTRA_FQDN] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra FQDN cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_key(self):
        del self.configuration.config[VECTRA_API_KEY]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra API key cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_key(self):
        self.configuration.config[VECTRA_API_KEY] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra API key cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_daily_threat_feed_id(self):
        del self.configuration.config[VECTRA_DAILY_THREAT_FEED_ID]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra daily threat feed ID cannot be empty.', str(context.exception))

    def test_validate_with_no_vectra_weekly_threat_feed_id(self):
        del self.configuration.config[VECTRA_WEEKLY_THREAT_FEED_ID]

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra weekly threat feed ID cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_daily_threat_feed_id(self):
        self.configuration.config[VECTRA_DAILY_THREAT_FEED_ID] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra daily threat feed ID cannot be empty.', str(context.exception))

    def test_validate_with_empty_vectra_weekly_threat_feed_id(self):
        self.configuration.config[VECTRA_WEEKLY_THREAT_FEED_ID] = ''

        with self.assertRaises(InvalidConfigurationException) as context:
            self.configuration.validate()
        self.assertEqual('The Vectra weekly threat feed ID cannot be empty.', str(context.exception))

    def test_get_cyjax_api_key(self):
        self.assertEqual('test-cyjax-key', self.configuration.get_cyjax_api_key())

    def test_get_vectra_fqdn(self):
        self.assertEqual('brain.vectra-fqdn.com', self.configuration.get_vectra_fqdn())

    def test_get_vectra_api_key(self):
        self.assertEqual('test-vectra-key', self.configuration.get_vectra_api_key())

    def test_get_vectra_threat_feed_id(self):
        self.assertEqual(('test-vectra-daily-feed-id', 'test-vectra-weekly-feed-id'),
                         self.configuration.get_vectra_threat_feed_ids())

    def test_get_vectra_ssl_verification(self):
        self.assertEqual(False, self.configuration.get_vectra_ssl_verification())

    def test_get_config_file_path(self):
        self.configuration.config_file_path = '/test/' + CONFIG_FILE_PATH
        self.assertEqual('/test/' + CONFIG_FILE_PATH, self.configuration.get_config_file_path())
