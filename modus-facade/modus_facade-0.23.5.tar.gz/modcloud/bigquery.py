"""Class to interact with BigQuery.

Uses google-cloud-bigquery
"""
import logging

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

logger = logging.getLogger(__name__)


class BigQuery(object):
    """Wrapper for google.cloud bigquery api."""

    def __init__(self, project_id):
        """Instantiate BigQuery."""
        self.client = bigquery.client.Client(project=project_id)
        self.SchemaField = bigquery.SchemaField
        self.project_id = project_id

    def dataset_exists(self, dataset_id):
        """Check if dataset exists.

        :param dataset_id: Name of dataset
        :type dataset_id: str
        :return: True if the dataset exists.
        :rtype: bool
        """
        dataset_ref = bigquery.DatasetReference(self.project_id, dataset_id)
        try:
            self.client.get_dataset(dataset_ref)  # Make an API request.
            logger.info(f"Dataset {dataset_id} already exists")
            return True
        except NotFound:
            logger.info(f"Dataset {dataset_id} is not found")
            return False

    def create_dataset(self, dataset_id, location='EU'):
        """Create the dataset with given name.

        :param dataset_id: Name of the dataset we create in.
        :type dataset_id: str
        :param location: Location where dataset should be created, default EU.
        :type location: str
        :return: None
        :rtype: None
        """
        dataset_ref = bigquery.DatasetReference(self.project_id, dataset_id)
        dataset = bigquery.Dataset(dataset_ref=dataset_ref)
        dataset.location = location

        # Raises google.api_core.exceptions.Conflict if the Dataset already
        # exists within the project.
        if self.dataset_exists(dataset_id):
            logger.warning(f"Dataset: {dataset_id} already exists in project")
        else:
            dataset = self.client.create_dataset(dataset_ref)
            logger.info(f"created dataset '{dataset.dataset_id}'")

    def table_exists(self, dataset_id, table_id):
        """Check if table exists.

        :param dataset_id: Dataset name.
        :type dataset_id: str
        :param table_id: Table name.
        :type table_id: str
        :return: True if table exists
        :rtype: bool
        """
        table = f"{self.project_id}.{dataset_id}.{table_id}"
        try:
            self.client.get_table(table)  # Make an API request.
            logger.info(f"Table {table} already exists.")
            return True
        except NotFound:
            logger.info(f"Table {table} is not found.")
            return False

    def create_table(self, dataset_id, table_id, schema=None):
        """Create a table.

        :param dataset_id: Dataset name.
        :type dataset_id: str
        :param table_id: Table name.
        :type table_id: str
        :param schema: List of Bigquery schema fields for table.
        :type schema: list
        :return: None
        :rtype: None
        """
        table = f"{self.project_id}.{dataset_id}.{table_id}"
        if self.table_exists(dataset_id, table_id):
            logger.warning(f"Table {table_id} in dataset {dataset_id} already exists")
        else:
            table_ref = bigquery.Table(table, schema=schema)
            self.client.create_table(table_ref)
            logger.info(f"created table '{table}'")

    def export_table_to_storage(self,
                                dataset_id,
                                table_id,
                                bucket,
                                file_location=None,
                                destination_format='CSV'
                                ):
        """Export a BigQuery table to Google Storage.

        :param dataset_id: BigQuery dataset name where source data resides.
        :type dataset_id: str
        :param table_id: BigQuery table name where source data resides.
        :type table_id: str
        :param bucket: Google Storage bucket where table gets saved.
        :type bucket: str
        :param file_location: Google Storage path after the bucket.
        :type file_location: str
        :param destination_format: CSV, NEWLINE_DELIMITED_JSON or AVRO
        :type destination_format: str
        :return: The random ID generated to identify the job.
        :rtype: str
        """
        destination_uri = f"gs://{bucket}/{file_location}/*"
        dataset_ref = bigquery.DatasetReference(self.project_id, dataset_id)
        table_ref = dataset_ref.table(f"{table_id}")
        table = self.client.get_table(table_ref)
        job_config = bigquery.job.ExtractJobConfig()
        job_config.destination_format = destination_format

        extract_job = self.client.extract_table(
            table_ref,
            destination_uri,
            job_config=job_config,
            # Location must match that of the source table.
            location=table.location
        )  # API request
        extract_job.result()  # Waits for job to complete.

    def stream_rows_to_table(self, dataset_id, table_id, rows, schema):
        """Stream a number of rows to BigQuery using the streaming api.

        :param dataset_id: Dataset ID of table we are writing to.
        :type dataset_id: str
        :param table_id: Table ID we are writing to.
        :type table_id: str
        :param rows: The data we are inserting
        :type rows: list of tuple
        :param schema: The table schema needed if the table does not exist yet.
        :type schema: list of bigquery.SchemaField
        :return: Errors if there are any.
        :rtype: list of dict
        """
        if len(rows) == 0:
            logger.warning("You have no data in 'rows'")
            return []
        if not isinstance(rows[0], tuple):
            logger.error(
                "Please ensure that your rows are a list of tuples.  "
                "Your schema needs to exist beforehand and conform to "
                "the strict rules set out in the google.cloud.bigquery api"
            )

        table = self.client.get_table(f'{self.project_id}.{dataset_id}.{table_id}')

        if self.table_exists(dataset_id, table_id):
            logger.info(
                "Table {}.{} already exists".format(dataset_id, table_id))
        else:
            logger.info("Creating {}.{}".format(dataset_id, table_id))
            table.schema = schema
            table.create()

        table_ref = self.client.get_table(table)
        logger.info("inserting data...")
        table_schema = table_ref.schema
        errors = self.client.insert_rows(table_ref, rows, selected_fields=table_schema)

        return errors

    def load_table_from_storage(self,
                                dataset_id,
                                table_id,
                                source_uri_pattern,
                                schema,
                                create_disposition="CREATE_IF_NEEDED",
                                write_disposition="WRITE_TRUNCATE",
                                source_format='NEWLINE_DELIMITED_JSON',
                                skip_leading_rows=None):
        """Load data from google storage into BigQuery.

        :param dataset_id: dataset_id name
        :type dataset_id: str
        :param table_id: table_id name
        :type table_id: str
        :param source_uri_pattern: UIR of form 'gs://bucket/file/abc-*
        :type source_uri_pattern: str
        :param schema: The provided schema as required by the api, refer to
          Google docs on syntax
        :type schema: list of SchemaField
        :param create_disposition: default CREATE_IF_NEEDED
        :type create_disposition: str
        :param write_disposition: default WRITE_TRUNCATE (WRITE_TRUNCATE, WRITE_APPEND,
                                  WRITE_EMPTY)
        :type write_disposition: str
        :param source_format: default NEWLINE_DELIMITED_JSON, else is CSV
        :type source_format: str
        :param skip_leading_rows: number of leading rows to skip for CSV format
        :type skip_leading_rows: int
        :return: Job ID
        :rtype: str
        """
        table = f"{self.project_id}.{dataset_id}.{table_id}"

        destination_dataset = self.client.get_dataset(dataset_id)

        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=source_format,
            write_disposition=write_disposition,
            create_disposition=create_disposition,
        )
        if skip_leading_rows:
            job_config.skip_leading_rows = skip_leading_rows

        load_job = self.client.load_table_from_uri(
            source_uri_pattern,
            table,
            # Must match the destination dataset location.
            location=destination_dataset.location,
            job_config=job_config,
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = self.client.get_table(table)
        logger.info("Loaded {} rows.".format(destination_table.num_rows))

        return load_job.job_id

    def execute_async_query_to_table(self,
                                     dataset_id,
                                     table_id,
                                     query,
                                     flatten_results=True,
                                     write_disposition="WRITE_TRUNCATE",
                                     use_legacy_sql=False,
                                     billing_tier=1):
        """Run a BigQuery query and save the results in BigQuery.

        :param dataset_id: Dataset name of resulting data.
        :type dataset_id: str
        :param table_id: Table name of resulting data.
        :type table_id: str
        :param query: The full query string
        :type query: str
        :param flatten_results: True to flatten results
        :type flatten_results: bool
        :param write_disposition: Default of WRITE_TRUNCATE
        :type write_disposition: str
        :param use_legacy_sql: True to use legacy sql
        :type use_legacy_sql: bool
        :param billing_tier: Maximum billing tier to use.
        :type billing_tier: int
        :return: Job name (ID)
        :rtype: str
        """
        job_config = bigquery.QueryJobConfig(
            destination=f"{self.project_id}.{dataset_id}.{table_id}",
            flatten_results=flatten_results,
            write_disposition=write_disposition,
            use_legacy_sql=use_legacy_sql,
            maximum_billing_tier=billing_tier
        )

        job = self.client.query(query, job_config=job_config)
        # Waits for job to complete
        job.result()

        return job.job_id

    def execute_synchronous_query(self, query, use_legacy_sql=False):
        """Run a query and save the results locally.

        :param query: Query to run
        :type query: str
        :param use_legacy_sql: True to use legacy sql
        :type use_legacy_sql: bool
        :return: A list of tuples with the query results
        :rtype: list of tuple or None
        """
        job_config = bigquery.QueryJobConfig(
            use_legacy_sql=use_legacy_sql
        )

        results = self.client.query(query, job_config=job_config)

        all_rows = []

        for row in results:
            all_rows.append(row.values())
        return all_rows

    def get_table_schema(self, dataset_id, table_id):
        """Get the google.cloud.schema for a given table.

        :param dataset_id: Dataset id
        :type dataset_id: str
        :param table_id: table id.
        :type table_id: str
        :return: The schema for a table
        :rtype: google.cloud.biguery.schema.SchemaField
        """
        table = self.client.get_table(f'{self.project_id}.{dataset_id}.{table_id}')
        return table.schema
