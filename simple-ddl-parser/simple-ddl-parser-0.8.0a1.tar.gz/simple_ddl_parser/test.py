from simple_ddl_parser import DDLParser


ddl = """
CREATE EXTERNAL TABLE IF NOT EXISTS database.table_name
(
    day_long_nm     string,
    calendar_dt     date,
    source_batch_id string,
    field_qty       decimal(10, 0),
    field_bool      boolean,
    field_float     float,
    create_tmst     timestamp,
    field_double    double,
    field_long      bigint
) PARTITIONED BY (batch_id int, batch_id2 string, batch_32 some_type) STORED AS PARQUET LOCATION 's3://datalake/table_name/v1'

"""


result = DDLParser(ddl).run(output_mode='hql')

print(result)