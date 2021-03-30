from src.configuration import Configuration, CYJAX_API_KEY, VECTRA_FQDN, VECTRA_DAILY_THREAT_FEED_ID, \
    VECTRA_WEEKLY_THREAT_FEED_ID, VECTRA_API_KEY, VECTRA_SSL_VERIFICATION


def create_mock_configuration():
    configuration = Configuration()
    configuration.config[CYJAX_API_KEY] = 'test-cyjax-key'
    configuration.config[VECTRA_FQDN] = 'brain.vectra-fqdn.com'
    configuration.config[VECTRA_API_KEY] = 'test-vectra-key'
    configuration.config[VECTRA_DAILY_THREAT_FEED_ID] = 'test-vectra-daily-feed-id'
    configuration.config[VECTRA_WEEKLY_THREAT_FEED_ID] = 'test-vectra-weekly-feed-id'
    configuration.config[VECTRA_SSL_VERIFICATION] = False
    configuration.config_path = '/tmp/'

    return configuration
