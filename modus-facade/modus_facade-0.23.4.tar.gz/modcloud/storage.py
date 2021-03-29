"""For working with google.cloud.storage.

https://google-cloud-python.readthedocs.io/en/latest/storage-client.html
https://pypi.python.org/pypi/google-cloud-storage
"""
import logging
import os
import shutil

from google.cloud import storage

logger = logging.getLogger(__name__)


class Storage(object):
    """Class to manage storage functions."""

    def __init__(self, project_id=None):
        """Initialize the storage object.

        :param project_id: Define project_id. Default system config if None
        :type project_id: str or None
        """
        self.client = storage.Client(project_id)

    def create_bucket(self, bucket_name):
        """Create a bucket in the default credentials project.

        :param bucket_name: The bucket name we want to create in our project.
        :type bucket_name: str
        :return: None
        :rtype: None
        """
        self.client.create_bucket(bucket_name)
        logger.info("created bucket '{}'".format(bucket_name))

    def bucket_exists(self, bucket_name):
        """Check if a bucket exists.

        :param bucket_name: The bucket name to check for existance.
        :type bucket_name: str
        :return: True if bucket exists in project.
        :rtype: bool
        """
        if self.client.lookup_bucket(bucket_name):
            return True
        return False

    def delete_bucket(self, bucket_name):
        """Delete the given bucket.

        :param bucket_name: The bucket name
        :type bucket_name: str
        :return: None
        :rtype: None
        """
        bucket = self.client.lookup_bucket(bucket_name)
        bucket.delete()

    def clear_bucket(self, bucket_name, blob_prefix=''):
        """Clear the bucket of all content within it.

        :param bucket_name: The bucket to clear.
        :type bucket_name: str
        :param blob_prefix: The prefix of all objects within the objects.
        :type blob_prefix: str
        :return: None
        :rtype: None
        """
        bucket = self.client.get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=blob_prefix)
        for blob in blobs:
            logger.info("deleting '{}'".format(blob.name))
            bucket.delete_blob(blob.name)

    def list_bucket(self, bucket_name, prefix=''):
        """List all of the items within a bucket.

        :param bucket_name: Name of the bucket
        :type bucket_name: str
        :param prefix: Prefix of the files for the bucket.
        :type prefix: str or None
        :return: List of items in bucket.
        :rtype: list of dict
        """
        blobs = self.client.lookup_bucket(
            bucket_name
        ).list_blobs(prefix=prefix)
        return [o.__dict__ for o in blobs]

    def copy_storage_dir_to_local(self,
                                  bucket_name,
                                  prefix,
                                  local_path,
                                  clear_local_first=True):
        """Copy data from cloud over to local.

        :param bucket_name: Bucket path where files are stored.
        :type bucket_name: str
        :param prefix: Storage prefix path where files are stored.
        :type prefix: str
        :param local_path: Local path where data is stored.
        :type local_path: str
        :param clear_local_first: True: we want to clear local directory first
        :type clear_local_first: bool
        :return: None
        :rtype: None
        """
        bucket = self.client.lookup_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)

        # clear the local directory first
        if clear_local_first and os.path.isdir(local_path):
            logger.info("clearing '{}'".format(local_path))
            shutil.rmtree(local_path)

        if not os.path.isdir(local_path):
            logger.info("creating '{}'".format(local_path))
            os.makedirs(local_path)

        for blob in blobs:
            if blob.name == prefix or blob.name.endswith("/"):
                # First blob is the folder
                continue

            filename = "{}".format(blob.name.split('/')[-1])
            source_name = "gs://{}/{}".format(bucket_name, blob.name)
            local_filename = os.path.join(local_path, filename)
            logger.info("Downloading '{}' to '{}'...".format(
                source_name,
                local_filename)
            )
            with open(local_filename, 'wb') as file_obj:
                blob.download_to_file(file_obj)

        logger.info("Finished copying storage files to local")

    def upload_object(self, local_path, bucket_name, prefix=''):
        """Upload the local model up to cloud storage.

        :param local_path: Local location of the file to upload.
        :type local_path: str
        :param bucket_name: Target google storage bucket for file.
        :type bucket_name: str
        :param prefix: Target gs 'prefix': The rest of the path after bucket.
        :type prefix: str
        :return: None
        :rtype: None
        """
        bucket = self.client.get_bucket(bucket_name)

        # If we have a directory, go through and get each file
        files_to_upload = []
        for root, subfolders, files in os.walk(local_path):
            for file in files:
                filepath = os.path.join(root, file)
                files_to_upload.append(filepath)

        # if we have a single file, then the list will be empty
        if not files_to_upload:
            files_to_upload.append(local_path)

        for upload_file in files_to_upload:
            filename = os.path.basename(upload_file)
            blob_name = os.path.join(prefix, filename)
            blob = bucket.blob(blob_name)
            try:
                blob.upload_from_filename(filename=upload_file)
                logger.info(
                    "uploaded '{}' to '{}'".format(upload_file, blob_name)
                )
            except FileNotFoundError:
                # in case there are temporary cached files
                logger.warning("'{}' not found".format(upload_file))
        logger.info("uploading '{}' done.".format(local_path))
