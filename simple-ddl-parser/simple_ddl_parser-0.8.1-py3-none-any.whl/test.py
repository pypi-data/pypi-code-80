from simple_ddl_parser import DDLParser


ddl = """
CREATE TABLE IF NOT EXISTS default.salesorderdetail(
        column_abc ARRAY <structcolx:string,coly:string> not null,
        employee_info STRUCT < employer: STRING, id: BIGINT, address: STRING >,
        employee_description string, 
        column_abc ARRAY<structcolx:string,coly:string>,
        column_map MAP < STRING, STRUCT < year: INT, place: STRING, details: STRING >>,
        column_map_no_spaces MAP<STRING,STRUCT<year:INT,place:STRING,details:STRING>>,
        column_struct STRUCT < street_address: STRUCT <street_number: INT, street_name: STRING, street_type: STRING>, country: STRING, postal_code: STRING >
        )
"""


result = DDLParser(ddl).run(output_mode='hql')
import pprint
pprint.pprint(result)