from ingestion.config.feed import Feed


class ConfigurationModel:
    def __init__(self, configuration):
        self.global_params = configuration['global_params']
        self.feeds = list(map(lambda feed_definition: Feed(feed_definition), configuration['feeds']))
