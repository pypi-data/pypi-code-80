import logging
from dataclasses import dataclass
from typing import List, Dict, Any

try:
    import asyncpg
except ImportError:
    print("Please install metaphor[postgresql] extra\n")
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
    ForeignKey,
    EntityType,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


@dataclass
class PostgresqlRunConfig(RunConfig):
    host: str
    database: str
    user: str
    password: str

    @staticmethod
    def parameters() -> List[str]:
        return ["host", "database", "user", "password"]

    @staticmethod
    def build(obj: Any) -> "RunConfig":
        return PostgresqlRunConfig(
            obj["host"], obj["database"], obj["user"], obj["password"]
        )


class PostgresqlExtractor(BaseExtractor):
    """PostgreSQL metadata extractor"""

    _ignored_dbs = ["template0", "template1", "rdsadmin"]

    def __init__(self):
        self._databases: List[str] = []
        self._table_columns: Dict[str, List] = {}
        self._table_constraints: Dict[str, List] = {}

    async def extract(self, config: PostgresqlRunConfig) -> List[Dataset]:
        logger.info("Fetching metadata from PostgreSQL host {}".format(config.host))

        conn = await self._connect_database(
            config.host, config.user, config.password, config.database
        )
        try:
            self._databases = await self._fetch_databases(conn)
            logger.info("Databases: {}".format(self._databases))
        finally:
            await conn.close()

        for db in self._databases:
            conn = await self._connect_database(
                config.host, config.user, config.password, db
            )
            try:
                tables = await self._fetch_tables(conn)
                logger.info("DB {} has tables {}".format(db, tables))

                # TODO: parallel fetching
                for schema, name in tables:
                    table_name = self._dataset_name(db, schema, name)
                    await self._fetch_columns(conn, schema, name, table_name)
                    await self._fetch_constraints(conn, schema, name, table_name)
            finally:
                await conn.close()

        logger.debug(self._table_columns)

        return self._build_entities()

    @staticmethod
    def _dataset_name(db: str, schema: str, table: str) -> str:
        return "{}.{}.{}".format(db, schema, table)

    @staticmethod
    async def _connect_database(host: str, user: str, password: str, database: str):
        logger.info("Connecting to DB {}".format(database))
        return await asyncpg.connect(
            host=host, user=user, password=password, database=database
        )

    @staticmethod
    async def _fetch_databases(conn) -> [str]:
        results = await conn.fetch("SELECT datname FROM pg_database")
        return [r[0] for r in results if r[0] not in PostgresqlExtractor._ignored_dbs]

    @staticmethod
    async def _fetch_tables(conn) -> [(str, str)]:
        tables = await conn.fetch(
            "SELECT table_catalog, table_schema, table_name "
            "FROM information_schema.tables "
            "WHERE table_type = 'BASE TABLE' AND table_schema != 'pg_catalog' "
            "  AND table_schema != 'information_schema' "
            "ORDER BY table_schema, table_name"
        )
        return [(t["table_schema"], t["table_name"]) for t in tables]

    async def _fetch_columns(self, conn, schema, name, table_name) -> None:
        self._table_columns[table_name] = await conn.fetch(
            "SELECT ordinal_position, cols.column_name, data_type, character_maximum_length, "
            "  numeric_precision, is_nullable, "
            "  pg_catalog.col_description(pgc.oid, cols.ordinal_position::int) as description "
            "FROM information_schema.columns AS cols "
            "LEFT OUTER JOIN pg_catalog.pg_class pgc "
            "  ON pgc.oid = (SELECT cols.table_name::regclass::oid) "
            "  AND pgc.relname = cols.table_name "
            "WHERE cols.table_schema = $1 AND cols.table_name = $2 "
            "ORDER BY ordinal_position",
            schema,
            name,
        )

    async def _fetch_constraints(self, conn, schema, name, table_name):
        self._table_constraints[table_name] = await conn.fetch(
            "SELECT constraints.constraint_name, constraints.constraint_type, "
            "  string_agg(key_col.column_name, ',') AS key_columns, "
            "  constraint_col.table_catalog AS constraint_db, "
            "  constraint_col.table_schema AS constraint_schema, "
            "  constraint_col.table_name AS constraint_table, "
            "  string_agg(constraint_col.column_name, ',') AS constraint_columns "
            "FROM information_schema.table_constraints AS constraints "
            "LEFT OUTER JOIN information_schema.key_column_usage AS key_col "
            "  ON constraints.table_schema = key_col.table_schema "
            "  AND constraints.constraint_name = key_col.constraint_name "
            "LEFT OUTER JOIN  information_schema.constraint_column_usage AS constraint_col "
            "  ON constraints.table_schema = constraint_col.table_schema "
            "  AND constraints.constraint_name = constraint_col.constraint_name "
            "WHERE constraints.table_schema =$1 AND constraints.table_name = $2 "
            "  AND constraints.constraint_type IN ('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY') "
            "GROUP BY constraints.constraint_name, constraints.constraint_type, constraint_col.table_catalog, "
            "  constraint_col.table_schema, constraint_col.table_name",
            schema,
            name,
        )

    def _build_entities(self) -> List[Dataset]:
        entities = []
        for table, columns in self._table_columns.items():
            dataset = Dataset()
            dataset.type = EntityType.DATASET
            dataset.logical_id = DatasetLogicalID()
            dataset.logical_id.platform = DataPlatform.POSTGRESQL
            dataset.logical_id.name = table

            dataset.schema = DatasetSchema()
            dataset.schema.schema_type = SchemaType.SQL
            dataset.schema.fields = [
                PostgresqlExtractor._build_field(col) for col in columns
            ]

            if table in self._table_constraints:
                dataset.schema.sql_schema = PostgresqlExtractor._build_sql_schema(
                    self._table_constraints[table]
                )

            entities.append(dataset)

        return entities

    @staticmethod
    def _build_field(column) -> SchemaField:
        field = SchemaField()
        field.field_path = column["column_name"]
        field.native_type = column["data_type"]
        field.nullable = column["is_nullable"] == "YES"
        field.description = column["description"]
        return field

    @staticmethod
    def _build_sql_schema(constraints: List) -> SQLSchema:
        schema = SQLSchema()
        for constraint in constraints:
            if constraint["constraint_type"] == "PRIMARY KEY":
                schema.primary_key = constraint["key_columns"].split(",")
            elif constraint["constraint_type"] == "FOREIGN KEY":
                foreign_key = ForeignKey()
                foreign_key.field_path = constraint["key_columns"]
                foreign_key.parent = DatasetLogicalID()
                foreign_key.parent.name = PostgresqlExtractor._dataset_name(
                    constraint["constraint_db"],
                    constraint["constraint_schema"],
                    constraint["constraint_table"],
                )
                foreign_key.parent.platform = DataPlatform.POSTGRESQL
                foreign_key.parent_field = constraint["constraint_columns"]

                if not schema.foreign_key:
                    schema.foreign_key = []
                schema.foreign_key.append(foreign_key)

        return schema
