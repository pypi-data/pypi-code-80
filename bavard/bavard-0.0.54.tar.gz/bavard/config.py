import os
import sys

from loguru import logger

IS_TEST = os.getenv("IS_TEST") == "true"
LOG_LEVEL = os.getenv("BAVARD_LOG_LEVEL", "INFO")

logger.remove()
logger.add(sys.stderr, level=LOG_LEVEL)
