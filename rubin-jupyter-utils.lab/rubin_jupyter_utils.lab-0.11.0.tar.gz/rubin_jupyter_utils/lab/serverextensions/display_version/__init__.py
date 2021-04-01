"""
Python module to initialize Server Extension for retrieving Rubin Observatory
settings.
"""
from .handlers import setup_handlers


def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{"module": "rubin_jupyter_utils.lab.serverextensions.display_version"}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info("Loading rubindisplayversion server extension.")
    setup_handlers(nbapp.web_app)
