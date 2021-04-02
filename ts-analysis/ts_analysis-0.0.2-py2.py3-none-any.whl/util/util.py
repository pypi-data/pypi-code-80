import logging
import logging.config
import os
import sys
from os import path

# Loggin Mix in rom https://blog.8bitzen.com/posts/12-07-2019-python-logging-mixin
__ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# adjust the below to place the log wherever you want to relative to this class
__TOP_LEVEL_PATH = path.join(__ROOT_DIR, '../../logs')

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] - %(module)s -  %(message)s",
    handlers=[
        #logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler("{0}/{1}.log".format(__TOP_LEVEL_PATH, "ts_analysis"))
    ])


# This class could be imported from a utility module
class LogMixin(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

    def log_stacktrace(self, message, error):
        self.logger.error(message)
        self.logger.exception(error)