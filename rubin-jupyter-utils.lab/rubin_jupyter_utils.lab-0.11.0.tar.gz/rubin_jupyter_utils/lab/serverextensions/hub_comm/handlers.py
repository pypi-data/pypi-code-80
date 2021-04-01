"""
This is a Handler Module to facilitate communication with JupyterHub in
the Rubin Observatory Science Platform context.
"""
import requests
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import APIHandler
from rubin_jupyter_utils.config import RubinConfig


class RubinHub_handler(APIHandler):
    """
    RubinHub Handler.  Currently all we do is DELETE (to shut down a running
    Lab instance) but we can extend this to do anything in the Hub REST API.
    """

    @property
    def lsstquery(self):
        return self.settings["lsstquery"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def delete(self):
        """
        Send a DELETE to the Hub API, which will result in this Lab
        instance being terminated (potentially, along with its namespace).

        We will need to make this more clever when and if we have multiple
        named servers.
        """

        cfg = RubinConfig()

        if not cfg.user:
            self.log.warning("User unknown; Hub communication impossible.")
            return
        if not cfg.hub_headers or not cfg.hub_headers['Authorization']:
            self.log.warning("Token unknown; Hub communication impossible.")
            return
        if not cfg.hub_api:
            self.log.warning("API URL unknown; Hub communication impossible.")
            return
        endpoint = ujoin(cfg.hub_api, "/users/{}/server".format(cfg.user))
        # Boom goes the dynamite.
        self.log.info("Requesting DELETE from {}".format(endpoint))
        requests.delete(endpoint, headers=cfg.hub_headers)


def setup_handlers(web_app):
    """
    Function used to setup all the handlers used.
    """
    # add the baseurl to our paths
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    handlers = [(ujoin(base_url, r"/rubin/hub"), RubinHub_handler)]
    web_app.add_handlers(host_pattern, handlers)
