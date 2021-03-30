import os
from .api_client import APIClientBase


class Virtualization(APIClientBase):
    def __init__(self, url_base=None, **kwargs):
        super().__init__(
            url_base or os.environ.get("VIRTUALIZATION_SERVICE", ""), **kwargs
        )

    def get_hypervisors(self):
        return self.get_request("/hypervisors")

    def get_vms(self):
        return self.get_request("/vms")

    def get_vmware_hosts(self):
        return self.get_request("/vmware/hosts")

    def get_vmware_datastores(self):
        return self.get_request("/vmware/datastores")

    def get_image_repository(self):
        return self.get_request("/image-repository")
