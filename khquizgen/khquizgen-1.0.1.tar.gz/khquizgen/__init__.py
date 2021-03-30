import os
import sys
import shutil
from pathlib import Path
from . src.utils import logger
from . src.utils import logger_b
from . src import parse_questions
from . src import gen_quiz
from . src import use_template
from . quizgen import main
from dynaconf import settings

# Set default path for package, ensuring that templates are accessible
PKGROOT = Path(__file__).resolve().parent
PKGINPUT = PKGROOT.joinpath('inputs')
PKGOUTPUT = PKGROOT.joinpath('outputs')
# Enable setting config if used as a standalone module
if '--config' in sys.argv:
    conf_path = sys.argv[sys.argv.index('--config') + 1]
    config_path = Path(conf_path).resolve()
    assert config_path.exists(), f"Config file not found on path {config_path}"
    assert '.toml' in config_path.suffix, "Config files need to be a valid .toml file, see example."
    os.environ['SETTINGS_FILE_FOR_DYNACON'] = str(config_path)
# Set default production environment if not specified in Envar
if os.getenv('ENV_FOR_DYNACONF') is None:
    os.environ['ENV_FOR_DYNACONF'] = 'production'
# Load config from dynaconf. If importing module, ensure you set root path in envar.
LOGPATH = Path(settings.LOGS).resolve()
LOGGING = settings.LOGGING
DEBUG = settings.DEBUG
INPUTS_PATH = Path(settings.INPUT).resolve()
OUTPUTS_PATH = Path(settings.OUTPUT).resolve()
logger.debug(f"Root Path ENVAR: {os.get('ROOT_PATH_FOR_DYNACONF')}")
logger.debug(f"Working env: {os.environ.get('ENV_FOR_DYNACONF')}")
__all__ = [
    'PKGROOT',
    'DEBUG',
    'INPUTS_PATH',
    'OUTPUTS_PATH',
    'parse_questions',
    'gen_quiz',
    'use_template',
    'logger',
    'logger_b',
    'main'
]


def printconfig(varname, var):
    logger.debug(f"__init__: Setting {varname} to {var}")


# DEBUG logging enabled
if DEBUG is True:
    logger = logger.bind(debug_off=False)
    if LOGGING:
        logs = LOGPATH.joinpath('q_compare.log')
        logger.add(LOGPATH, rotation="5 MB", level="TRACE",
                   format="{message}",
                   filter=lambda record: record["extra"].get("name") == "b")


logger.info("Initialization in progress")
logger.debug("Debug mode on.")
printconfig('PKGROOT', PKGROOT)
printconfig('PKGINPUT', PKGINPUT)
printconfig('INPUTS_PATH', INPUTS_PATH)
printconfig('OUTPUTS_PATH', OUTPUTS_PATH)
printconfig('LOGS', LOGPATH)
