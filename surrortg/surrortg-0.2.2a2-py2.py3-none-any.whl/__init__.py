"""surrortg"""

import pkg_resources

from .config_parser import get_config
from .game import Game, RobotType
from .game_io import GameIO
from .network.ge_api_client import ApiClient

__version__ = "0.2.2a2"
