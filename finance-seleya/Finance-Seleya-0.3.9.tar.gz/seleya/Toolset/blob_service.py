import os
from azure.storage.blob import BlockBlobService

class BlobService(object):
    def __init__(self):
        self._block_blob_service = BlockBlobService(
        account_name=os.environ['seleya_azure_user'],
        account_key=os.environ['seleya_azure_key'])
        
    def upload_file(self, container_name, local_file_name, remote_file_name):
        return self._block_blob_service.create_blob_from_path(
            container_name, remote_file_name, local_file_name)
    
    def download_file(self, container_name, remote_file_name, local_file_name):
        return self._block_blob_service.get_blob_to_path(
            container_name, remote_file_name, local_file_name)  