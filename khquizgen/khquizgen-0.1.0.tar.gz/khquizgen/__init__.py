import os
import sys
import shutil
from pathlib import Path
from loguru import logger

PKGROOT = Path(__file__).resolve().parent
if '--config' in sys.argv:
    ConfigParam = sys.argv[sys.argv.index('--config') + 1]
    ConfigPath = Path(ConfigParam).resolve()
    assert ConfigPath.exists(), f"Config file not found on path {ConfigPath}"
    assert '.ini' in ConfigPath.suffix, "Config files need to be a valid .ini file, see example."
    try:
        shutil.copyfile(ConfigPath, PKGROOT.joinpath('config', 'config.ini'))
    except OSError as err:
        logger.critical(f"OS Error: {err}")
        exit(-1)
from khquizgen.config import CONFIG

# Set up logging filter. Later check if DEBUG_PATH set, if it is, we switch back to debug
def my_filter(record):
    if record["extra"].get("debug_off"):  # "warn_only" is bound to the logger and set to 'True'
        return record["level"].no >= logger.level("INFO").no
    return True  # Fallback to default 'level' configured while adding the handler


# Initial setup for loggers.
logger.remove(0)
logger.add(sys.stderr, filter=my_filter, level="DEBUG")
logger = logger.bind(debug_off=True)


LOGPATH = CONFIG.get_log_path(PKGROOT)


# ANSI colour escape codes (for use in logging/debug messages)
class ANSI:
    RED = '\033[91m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    RESET = '\033[39m'


if not os.getenv('VIRTUAL_ENV'):
    logger.warning(f"""{ANSI.PURPLE}
Warning: No suitable VIRTUAL_ENV environmental variable detected.

In order to ensure consistency / reproducibility between runs, you might want to
consider always running this package from within a suitable python virtual
environment, containing the python package versions specified in the package's
requirements.txt file.

Press ENTER if you'd like to continue regardless (or Ctrl-C to abort)

{ANSI.RESET}""")
    try:
        input()   # i.e. press Enter
    except KeyboardInterrupt:
        logger.warning('\n\nExiting...')
        exit()


# Import all configuration constants
DEBUG = CONFIG.DEBUG
INPUTS_PATH = CONFIG.get_inputs_path(PKGROOT)
OUTPUTS_PATH = CONFIG.get_outputs_path(PKGROOT)


def printconfig(varname, var):
    logger.debug(f"{ANSI.BLUE}__init__: Setting {varname} to {ANSI.ORANGE}{var}{ANSI.RESET}")


if DEBUG not in [True, False]:
    raise ValueError('Bad value given for DEBUG_APP environmental variable. \
                        Needs to be True or False.')


# DEBUG logging enabled
if DEBUG is True:
    logger = logger.bind(debug_off=False)
    logger.add(LOGPATH, rotation="5 MB", level="TRACE",
               format="{message}",
               filter=lambda record: record["extra"].get("name") == "b")

logger_b = logger.bind(name="b")
logger.info("Initialization in progress")
logger.debug("Debug mode on.")
printconfig('PKGROOT', PKGROOT)
printconfig('INPUTS_PATH', INPUTS_PATH)
printconfig('OUTPUTS_PATH', OUTPUTS_PATH)


__all__ = [
    'PKGROOT',
    'DEBUG',
    'INPUTS_PATH',
    'OUTPUTS_PATH',
    'logger'
]
