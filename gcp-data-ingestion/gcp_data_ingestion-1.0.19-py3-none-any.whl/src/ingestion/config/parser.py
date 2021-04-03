import yaml

from ingestion.config.model import ConfigurationModel

"""
This class loads the application configuration file (config.yaml)
as a stream / YAML String and exposes the configuration via its
model attribute.
"""


class ConfigurationParser:

    def __init__(self, stream):
        self.dictionary = yaml.safe_load(stream)
        self.model = ConfigurationModel(self.dictionary)
