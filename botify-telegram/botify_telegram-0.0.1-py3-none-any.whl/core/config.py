import os
import json
import yaml
from os import path
from ..utils import Container, BotifyLogger

class BotifyConfig(Container):

    def __init__(self, botify, **kwargs):
        super().__init__(**kwargs)

        self.botify = botify
        self.logger = BotifyLogger("config")
        logger = self.logger

        config_folder_path = path.join(
            os.getcwd(),
            "config"
        )

        if path.exists(config_folder_path):
            logger.info(f"Found config [{config_folder_path}]")
            for entity in os.listdir(config_folder_path):
                entity_path = path.join(config_folder_path, entity)
                if path.isfile(entity_path):
                    
                    if entity.endswith(".json"):
                        logger.info(f"Loading data from {entity}")
                        with open(entity_path, encoding = "utf-8") as _file:
                            data = json.load(_file)
                            self.deep_update(data if data else {})

                    if entity.endswith(".yaml") or entity.endswith(".yml"):
                        logger.info(f"Loading data from {entity}")
                        with open(entity_path, encoding = "utf-8") as _file:
                            data = yaml.full_load(_file)
                            self.deep_update(data if data else {})      
                    
        else: raise OSError("Botify config folder does not exist. Please make it and run bot again.")