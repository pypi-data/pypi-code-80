import numpy as np
import pandas as pd
from datetime import datetime


class GCSUtils:

    @staticmethod
    def read_csv(blob_uri, feed, is_historical):
        if is_historical:
            col_names = feed.source_columns_historical
            delimiter = feed.field_delimiter_historical
        else:
            col_names = feed.source_columns
            delimiter = feed.field_delimiter
        df = pd.read_csv(blob_uri, encoding=feed.file_encoding, sep=delimiter, quoting=1, skiprows=1,
                         quotechar='"', converters={i: str for i in range(0, 100)}, names=col_names)
        return df

    @staticmethod
    def remove_extra_quotes(dataframe):
        dataframe_all_string_cols = dataframe.astype(str).replace('nan', np.nan)
        dataframe_with_quotes_removed = dataframe_all_string_cols.applymap(
            lambda x: x.replace('"', '')
            if (isinstance(x, str)) else x
        )
        return dataframe_with_quotes_removed

    @staticmethod
    def add_tracking_columns(dataframe, input_file_name, archive_file_name):
        """
                Adds two extra columns to every dataframe object for the purpose
                of data lineage.
                1. INPUT_FILE_NAME (for incremental and historical loads)
                2. ARCHIVE_FILE_NAME (for historical loads only)
        """

        dataframe['INPUT_FILE_NAME'] = input_file_name
        dataframe['ARCHIVE_FILE_NAME'] = archive_file_name
        return dataframe

    def __init__(self, storage_client, bucket_name):
        """
        Initialize the class with the storage client instance and the bucket name
        for performing listing blobs in the bucket.
        :param storage_client: storage.Client() instance
        :param bucket_name: The name of the bucket
        """
        self.client = storage_client
        self.bucket_name = bucket_name

    def list_blobs(self, feed):

        """
        Data Ingestion has to accommodate two types of data loads viz.
        1. Historical Data Load
        2. Incremental Data Load (BAU)

        In GCS, the files are organized based on the following path convention.

        <bucket_name>/raw/<source_system>/<dataset group>/<feed>/<file>
        eg.
        ecommerce-data-ingestion/raw/sap/product/makt/MAKT_<timestamp>.CSV
        ecommerce-data-ingestion/raw/sap/product/makt/historical/MAKT_<timestamp>.CSV



        :param feed: An Instance of the Feed Class
        :return: A List of blob objects that satisfies the parameter file_path_prefix
                 and file extension attributes defined in the Feed Instance parameter.
        """
        try:
            blobs_incremental = self.client.list_blobs(self.bucket_name, prefix=feed.file_path_prefix,
                                                       delimiter="/")
            filtered_blobs_incremental = list(filter(lambda b: b.name.upper().endswith(feed.file_extension),
                                                     blobs_incremental))

            prefix = feed.file_path_prefix + "historical/"
            blobs_historical = self.client.list_blobs(self.bucket_name, prefix=prefix,
                                                      delimiter="/")
            filtered_blobs_historical = list(filter(lambda b: b.name.upper().endswith(feed.file_extension),
                                                    blobs_historical))
            return filtered_blobs_historical, filtered_blobs_incremental
        except Exception as e:
            print(e.__cause__)

    @staticmethod
    def add_missing_columns(dataframe, feed, missing_columns):
        clone = dataframe.copy()
        for column in missing_columns:
            col_value = feed.default_value_for_missing_columns[column]
            clone[column] = col_value
        return clone

    """
        Moves blobs in GCS bucket from raw/{blob path} to archive/{yyyyMMdd}/{blob path}
    """
    def archive_blob(self, blob):
        today = datetime.today().strftime('%Y%m%d')
        tmp = "/".join(blob.name.split("/")[1::])
        blob_destination = f"archive/{today}/{tmp}"
        bucket = self.client.get_bucket(self.bucket_name)
        bucket.copy_blob(blob, bucket, blob_destination)
        blob.delete()
