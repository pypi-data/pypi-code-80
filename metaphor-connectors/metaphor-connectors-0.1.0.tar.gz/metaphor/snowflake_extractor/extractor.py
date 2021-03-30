import logging
from dataclasses import dataclass
from typing import List, Any, Dict

try:
    import snowflake.connector
except ImportError:
    print("Please install metaphor[snowflake] extra\n")
    raise

from metaphor.common.extractor import BaseExtractor, RunConfig
from metaphor.common.metadata_change_event import (
    Dataset,
    DatasetLogicalID,
    DatasetSchema,
    SchemaField,
    DataPlatform,
    SchemaType,
    SQLSchema,
    MaterializationType,
    EntityType,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class SnowflakeRunConfig(RunConfig):
    account: str
    user: str
    password: str
    database: str

    @staticmethod
    def parameters() -> List[str]:
        return ["account", "user", "password", "database"]

    @staticmethod
    def build(obj: Any) -> "SnowflakeRunConfig":
        return SnowflakeRunConfig(
            obj["account"], obj["user"], obj["password"], obj["database"]
        )


class SnowflakeExtractor(BaseExtractor):
    """Snowflake metadata extractor"""

    def __init__(self):
        self._datasets: Dict[str, Dataset] = {}

    async def extract(self, config: SnowflakeRunConfig) -> List[Dataset]:
        logger.info(f"Fetching metadata from Snowflake account {config.account}")
        ctx = snowflake.connector.connect(
            account=config.account, user=config.user, password=config.password
        )

        with ctx:
            cursor = ctx.cursor()

            databases = self._fetch_databases(cursor, config.database)
            logger.info(f"Databases: {databases}")

            # TODO: parallel fetching
            for db in databases:
                tables = self._fetch_tables(cursor, db)
                logger.info(f"DB {db} has tables {tables}")

                for schema, name, full_name in tables:
                    dataset = self._datasets[full_name]
                    self._fetch_columns(cursor, schema, name, dataset)
                    self._fetch_ddl(cursor, schema, name, dataset)

        logger.debug(self._datasets)

        return list(self._datasets.values())

    @staticmethod
    def _table_fullname(db: str, schema: str, name: str):
        """The full table name including database, schema and name"""
        return f"{db}.{schema}.{name}"

    @staticmethod
    def _fetch_databases(cursor, initial_database: str) -> [str]:
        cursor.execute("USE " + initial_database)
        cursor.execute(
            "SELECT database_name FROM information_schema.databases ORDER BY database_name"
        )
        return [db[0] for db in cursor]

    def _fetch_tables(self, cursor, database: str) -> [(str, str, str)]:
        cursor.execute("USE " + database)
        cursor.execute(
            "SELECT table_schema, table_name, table_type "
            "FROM information_schema.tables "
            "WHERE table_schema != 'INFORMATION_SCHEMA' "
            "ORDER BY table_schema, table_name"
        )

        tables: [(str, str, str)] = []
        for schema, name, table_type in cursor:
            full_name = self._table_fullname(database, schema, name)
            self._datasets[full_name] = self._init_dataset(full_name, table_type)
            tables.append((schema, name, full_name))

        return tables

    @staticmethod
    def _fetch_columns(cursor, schema: str, name: str, dataset: Dataset) -> None:
        cursor.execute(
            "SELECT ordinal_position, column_name, data_type, character_maximum_length, "
            "  numeric_precision, is_nullable, column_default, comment "
            "FROM information_schema.columns "
            "WHERE table_schema = %s AND table_name = %s "
            "ORDER BY ordinal_position",
            (schema, name),
        )
        for column in cursor:
            dataset.schema.fields.append(SnowflakeExtractor._build_field(column))

    @staticmethod
    def _fetch_ddl(cursor, schema: str, name: str, dataset: Dataset) -> None:
        try:
            cursor.execute("SELECT get_ddl('table', %s)", f"{schema}.{name}")
            dataset.schema.sql_schema.table_schema = cursor.fetchone()[0]
        except Exception as e:
            logger.error(e)

    @staticmethod
    def _init_dataset(full_name: str, table_type: str) -> Dataset:
        dataset = Dataset()
        dataset.type = EntityType.DATASET
        dataset.logical_id = DatasetLogicalID()
        dataset.logical_id.platform = DataPlatform.SNOWFLAKE
        dataset.logical_id.name = full_name

        dataset.schema = DatasetSchema()
        dataset.schema.schema_type = SchemaType.SQL
        dataset.schema.fields = []
        dataset.schema.sql_schema = SQLSchema()
        dataset.schema.sql_schema.materialization = (
            MaterializationType.VIEW
            if table_type == "VIEW"
            else MaterializationType.TABLE
        )

        return dataset

    @staticmethod
    def _build_field(column) -> SchemaField:
        field = SchemaField()
        field.field_path = column[1]
        field.native_type = column[2]
        field.nullable = column[5] == "YES"
        field.description = column[7]
        return field
