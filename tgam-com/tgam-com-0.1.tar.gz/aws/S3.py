import boto3
import os
from botocore.exceptions import ClientError
from src.config import Constants
from src.log.logger import Log


class S3Repository(object):
    def __init__(self):
        log_level = os.environ.get(Constants.LOG_LEVEL_ENV_KEY, Constants.DEFAULT_LOG_LEVEL)
        self.logger = Log(Constants.APP_NAME, log_level).get_logger()
        self.s3_client = boto3.client('s3', region_name=os.environ[Constants.AWS_REGION_ENV_KEY])

    def download_file(self, bucket_name, key):
        try:
            self.s3_client.download_file(bucket_name, key, Constants.MODEL_TMP_PATH)
        except ClientError as e:
            self.logger.error(f"Failed to download model from {bucket_name}/{key}  {e}")
            raise e

    def get_obj(self, bucket_name, key):
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=key)
        return obj["Body"]
