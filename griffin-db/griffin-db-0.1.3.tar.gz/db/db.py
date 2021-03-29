import psycopg2
from psycopg2.extras import execute_values as p_execute_values
import queries
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2

session = queries.Session(
    queries.uri(
        os.environ.get('PGHOST'),
        os.environ.get('PGPORT'),
        os.environ.get('PGDATABASE'),
        os.environ.get('PGUSER'),
        os.environ.get('PGPASSWORD'),
    ))

print("Database connected")

query = session.query


def execute_values(query, values):
    return p_execute_values(session.cursor, query, values)


def insert_value_from_dict(table_name, dictionary, extra_query=''):
    keys = dictionary.keys()

    # TODO: table_name and dictionary.keys and extra_query MUST be constants (sql injection opportunity)
    execute_values(
        'INSERT INTO ' + table_name + ' (' + ','.join(keys) + ') \
                        VALUES %s ' + extra_query, [list(dictionary.values())])


def insert_values_from_dicts(table_name, dictionaries, extra_query=''):
    if not dictionaries:
        return

    # Verify that all dictionaries have identical keys
    if not all(x.keys() == dictionaries[0].keys() for x in dictionaries):
        raise ValueError("Dictionaries have different keys")

    keys = dictionaries[0].keys()

    # TODO: table_name and dictionary.keys and extra_query MUST be constants (sql injection opportunity)
    execute_values(
        'INSERT INTO ' + table_name + ' (' + ','.join(keys) + ') \
                        VALUES %s ' + extra_query,
        (list(x.values()) for x in dictionaries))
