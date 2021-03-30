SQL = {
    "TABLES":
        {
            "MYSQL": """
                        Select table_name,TABLE_COMMENT AS comment from INFORMATION_SCHEMA.TABLES 
                        Where table_schema = :db_name
                     """,
            "ORACLE": """
                    select table_name,comment from user_tab_comments order by table_name 
                    """
        },
    "COLUMNS": {
        "MYSQL": """
                       SELECT
                           COLUMN_NAME as column_name,
                            DATA_TYPE as data_type,
                            IFNULL(column_Comment,COLUMN_NAME) as comment,
                            ifnull(character_maximum_length,concat(numeric_precision,',',NUMERIC_SCALE)) as data_length
                        
                        
                         from INFORMATION_SCHEMA.COLUMNS t
                         Where table_name = :table_name AND 
                         table_schema = :db_name
                        AND (`COLUMN_KEY` != 'PRI')
                     """,
        "ORACLE": """
                    select
                     tc.column_name,
                     data_type,
                     cc.comments as comment,
                     data_length,
                     data_precision,
                     
                     
                     tc.data_default
                     from  user_tab_columns tc left join user_col_comments cc 
                     on tc.TABLE_NAME=cc.table_name and tc.COLUMN_NAME=cc.column_name
                     where tc.TABLE_NAME=:table_name
                    """
    },

}
