"""
Python module to initialize Server Extension for Rubin Observatory JupyterHub
interaction.
"""
from .handlers import setup_handlers


def _jupyter_server_extension_paths():
    """
    Function to declare Jupyter Server Extension Paths.
    """
    return [{"module": "rubin_jupyter_utils.lab.serverextensions.hub_comm", }]


def load_jupyter_server_extension(nbapp):
    """
    Function to load Jupyter Server Extension.
    """
    nbapp.log.info("Loading Rubin hub_comm server extension.")
    setup_handlers(nbapp.web_app)
