import os
from .api_client import APIClientBase


class Virtualization(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(
            url_base or os.environ.get("VIRTUALIZATION_SERVICE", ""), **kwargs
        )

    def get_hypervisors(self):
        return self.get_request("/hypervisors/")

    def get_vms(self):
        return self.get_request("/hypervisors/vms")

    def get_hosts(self):
        return self.get_request("/hypervisors/hosts")

    def get_datastores(self):
        return self.get_request("/hypervisors/datastores")
