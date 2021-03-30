import sys

from loguru import logger
from toolz import curry

from .commands import ShellCommands
from .paths import get_build_folder, get_docker_file, get_stack_settings

shells = ShellCommands()

logger.configure(
    handlers=[
        dict(sink=sys.stdout),
        dict(sink=sys.stderr),
        dict(sink="file.log", enqueue=True, serialize=True),
    ],
    levels=[dict(name="BASH", no=44, icon="@", color="<fg #9600fa><bold>")],
)

# logger

# bash_log = curry(logger.opt(colors=True).log)
# bash_log = bash_log()
