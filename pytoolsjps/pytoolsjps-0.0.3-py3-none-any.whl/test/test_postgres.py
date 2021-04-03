import logging
import pytest
from datetime import datetime
import pandas as pd
from pytoolsjps.postgres import Connection, to_sql, insert_returning, bulk_insert

schema = 'my_schema'
table = 'my_table'


@pytest.fixture(scope='function')
def database():
    with Connection() as con:
        with con.cursor() as cur:

            try:
                cur.execute(f"""CREATE SCHEMA {schema};""")

                cur.execute(f"""CREATE TABLE {schema}.{table} (
                id serial PRIMARY KEY, 
                col_num integer, 
                col_str varchar,
                col_tms timestamp
                );""")
            except Exception as e:
                logging.exception(e)

    yield

    with Connection() as con:
        with con.cursor() as cur:
            try:
                cur.execute(f"""drop TABLE {schema}.{table};""")
                cur.execute(f"""drop SCHEMA {schema};""")
            except Exception as e:
                logging.exception(e)


df = pd.DataFrame({'col_num': 1,
                   'col_str': 'my_string',
                   'col_tms': [datetime.utcnow()]}
                  )


def test_insert_1_to_sql(database):
    """insert data (scenario 1) => pd.to_sql (with engine) for small dfs"""

    to_sql(df, table, schema)

    sql = f"select * from {schema}.{table}"
    with Connection() as con:
        df_ = pd.read_sql(sql, con)
        assert df_.loc[0, 'id'] == 1


def test_insert_2_with_returning(database):
    """insert data (scenario 2) => return primary key (for dataframes with one row)"""

    with Connection() as con:
        id = insert_returning(df, table, schema, con)
        assert id == 1


def test_insert_2_with_returning_throws(database):
    """insert_return_pk should raise exception when inserting multiple rows"""
    with pytest.raises(Exception):
        with Connection() as con:
            insert_returning(pd.concat([df, df]), table, schema, con)


def test_insert_3_bulk(database):
    """insert data (scenario 3) => bulk insert"""
    count_rows = 1000
    with Connection() as con:
        bulk_insert(pd.concat([df] * count_rows), table, schema, con)

        sql = f"select * from  {schema}.{table}"
        df_ = pd.read_sql(sql, con)
        assert len(df_) == count_rows


def test_select_1_read_sql(database):
    """read data (scenario 1) => pd.read_sql() with connection"""

    to_sql(df, table, schema)

    sql = f"select * from  {schema}.{table}"
    with Connection() as con:
        df_ = pd.read_sql(sql, con)
        assert df_.loc[0, 'id'] == 1


def test_select_2_cursor(database):
    """read data (scenario 2) => read via cursors"""

    to_sql(df, table, schema)

    sql = f"select * from  {schema}.{table}"

    with Connection() as con:
        with con.cursor() as cur:
            cur.execute(sql)
            results = cur.fetchall()
            assert results[0][0] == 1

        with con.cursor() as cur:
            cur.execute(sql)
            results = cur.fetchall()
            assert results[0][0] == 1


def test_update_1_cursor(database):
    """update data (scenario 1) => with cursor"""

    to_sql(df, table, schema)

    with Connection() as con:
        sql = f"select * from  {schema}.{table}"
        df_ = pd.read_sql(sql, con)
        assert df_.loc[0, 'id'] == 1

        sql_update = f"update {schema}.{table} set col_num = (%s) where id = (%s)"
        with con.cursor() as cur:
            params = (2, 1)
            cur.execute(sql_update, params)
            # naming params via dict seems not possible => https://www.postgresqltutorial.com/postgresql-python/update/

        # with Connection(postgres_con) as con:
        df_ = pd.read_sql(sql, con)
        assert df_.loc[0, 'col_num'] == 2
