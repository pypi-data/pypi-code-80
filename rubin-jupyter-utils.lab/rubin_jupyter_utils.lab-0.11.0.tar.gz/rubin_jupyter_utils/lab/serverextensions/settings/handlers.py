"""
This is a Handler Module to facilitate communication with JupyterHub in
the Rubin Observatory Science Platform context.
"""
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import APIHandler
from rubin_jupyter_utils.config import RubinConfig


class RubinSettings_handler(APIHandler):
    """
    RubinSettings Handler.  Return the JSON representation of our
    Rubin-specific settings.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rubin_config = RubinConfig()

    def get(self):
        """
        """
        self.log.info("Sending Rubin settings")
        self.finish(self.rubin_config.dump())


def setup_handlers(web_app):
    """
    Function used to setup all the handlers used.
    """
    # add the baseurl to our paths
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    handlers = [(ujoin(base_url, r"/rubin/settings"), RubinSettings_handler)]
    web_app.add_handlers(host_pattern, handlers)
