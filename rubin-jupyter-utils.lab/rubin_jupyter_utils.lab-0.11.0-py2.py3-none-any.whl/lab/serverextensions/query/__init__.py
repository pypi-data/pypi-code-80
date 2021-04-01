"""
Python module to initialize Rubin Jupyter Server Query Extension
"""
from .handlers import setup_handlers


def _jupyter_server_extension_paths():
    """
    Function to declare Rubin Jupyter Server Query Extension Paths.
    """
    return [{"module": "rubin_jupyter_utils.lab.serverextensions.query"}]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info("Loading Rubin Jupyter server Query extension.")
    setup_handlers(nbapp.web_app)
