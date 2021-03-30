from logging import Logger
from databricksbundle.notebook.decorator.DecoratedDecorator import DecoratedDecorator
from databricksbundle.notebook.decorator.ResultProcessingDecorator import ResultProcessingDecorator
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from datalakebundle.table.TableManager import TableManager


@DecoratedDecorator
class table_writer(ResultProcessingDecorator):  # noqa: N801
    def __init__(self, table_identifier: str, overwrite=False):
        self.__table_identifier = table_identifier
        self.__overwrite = overwrite

    def process_result(self, result: DataFrame, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")
        table_manager: TableManager = container.get(TableManager)

        output_table_name = table_manager.get_name(self.__table_identifier)

        logger.info(f"Data to be persisted into table: {output_table_name}")

        if self.__overwrite:
            table_manager.recreate(self.__table_identifier)
        else:
            table_manager.create_if_not_exists(self.__table_identifier)

        schema = table_manager.get_config(self.__table_identifier).schema

        self.__write(result, output_table_name, schema, logger)

    def __write(self, result: DataFrame, output_table_name: str, schema: StructType, logger: Logger):
        logger.info(f"Saving data to table: {output_table_name}")

        fields = [field.name for field in schema.fields]

        (result.select(fields).write.option("partitionOverwriteMode", "dynamic").insertInto(output_table_name))

        logger.info(f"Data successfully saved to: {output_table_name}")
