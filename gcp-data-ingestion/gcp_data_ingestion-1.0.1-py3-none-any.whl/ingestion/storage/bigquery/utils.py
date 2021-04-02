from google.cloud import bigquery
from google.cloud.exceptions import Conflict
import pandas_gbq


class BQUtils:

    @staticmethod
    def convert_type_to_bigquery(kind):
        type_mapping = {
            "i": "INTEGER",
            "b": "BOOLEAN",
            "f": "FLOAT",
            "O": "STRING",
            "S": "STRING",
            "U": "STRING",
            "M": "TIMESTAMP",
        }
        return type_mapping.get(kind, "STRING")

    @staticmethod
    def get_schema(dataframe):
        table_schema = []
        for key, value in dict(dataframe.dtypes).items():
            table_schema.append(bigquery.SchemaField(key, BQUtils.convert_type_to_bigquery(value.kind)))
        return table_schema

    def __init__(self, model):
        self.client = bigquery.Client(model.global_params['project_id'])
        self.model = model

    def load_data_into_bigquery(self, dataframe, table_name):
        dataset_id = self.model.global_params['target_dataset_id']
        pandas_gbq.to_gbq(dataframe, destination_table=f"{dataset_id}.{table_name}",
                          project_id=self.model.global_params['project_id'],
                          if_exists="append")

    def create_dataset(self):
        client = self.client
        dataset_id = f"{client.project}.{self.model.global_params['target_dataset_id']}"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = f"{self.model.global_params['bigquery_dataset_location']}"
        try:
            client.create_dataset(dataset, timeout=30)  # Make an API request.
            print("Created dataset {}.{}".format(client.project, dataset_id))
        except Conflict:
            print(f"Dataset {dataset_id} already exists.")

    def extract_table_definition_from_bigquery(self, project_id, dataset_id, table_id):
        client = self.client
        table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")
        return table

    @staticmethod
    def get_missing_columns(incoming_schema, table_schema):
        missing_fields = []
        for schema_field in table_schema:
            counter = 0
            for k, v in incoming_schema:
                if k == schema_field.name:
                    counter = 1
                    break
            if counter == 0:
                missing_fields.append(schema_field.name)
        return missing_fields

    def create_table(self, schema, table_name):
        client = self.client
        project = client.project
        dataset_ref = bigquery.DatasetReference(project, self.model.global_params['target_dataset_id'])
        table_ref = dataset_ref.table(table_name)
        table = bigquery.Table(table_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning()
        table.clustering_fields = ['INPUT_FILE_NAME']
        table = client.create_table(table, exists_ok=True)
        print(
            "Created table {}, partitioned on column {}".format(
                table.table_id, table.time_partitioning.field
            )
        )

    def get_rows_ingested_from_bigquery(self, project_id, dataset_id, table_name, file_name):
        query = f"select _partitiontime as pt from {project_id}.{dataset_id}.{table_name} where " \
                  f"input_file_name='{file_name}'"
        client = self.client
        job = client.query(query)
        results = job.result()
        print(f"Rows Count :{results.total_rows} for input file :{file_name}")
        return results.total_rows
