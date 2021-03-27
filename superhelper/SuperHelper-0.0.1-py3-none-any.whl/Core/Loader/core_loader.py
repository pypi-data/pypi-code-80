# This module defines the module loader function.
import importlib
import logging
from typing import List

from SuperHelper.Core.Helper import load_cli_config
from SuperHelper.Core.Helper.IO import print_error

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cli_config = load_cli_config()


def load_installed_modules() -> List:
    module_entries = []
    for module_name in cli_config["INSTALLED_MODULES"]:
        try:
            module_entries.append(importlib.import_module(module_name).main)
        except ImportError:
            logger.exception(f"Cannot import module '{module_name}'!")
            print_error(f"Cannot import module '{module_name}'!")
    return module_entries
