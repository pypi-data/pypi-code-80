"""Create a sql script with a variable month rolling window table query.

Then Execute using facade
"""
import datetime

from modcloud import BigQuery
from modlog import bootstrap_logging

logger = bootstrap_logging(
    'create_table_over_period',
    root_level="DEBUG",
)


def create_table_over_period(project_id,
                             source_query_path,
                             target_dataset_id,
                             target_table_id,
                             source_dataset_id,
                             source_table_id_prefix,
                             period,
                             use_legacy_sql=True,
                             write_disposition="WRITE_TRUNCATE"):
    """Execute the sql scrip after adding table query.

    :param project_id: name of project
    :type project_id: str
    :param source_query_path: path to source query after
      `containers/dag/code/queries/`
    :type source_query_path: str
    :param target_dataset_id: target dataset name
    :type target_dataset_id: str
    :param target_table_id: target table name
    :type target_table_id: str
    :param source_dataset_id: name of source dataset
    :type source_dataset_id: str
    :param source_table_id_prefix: name of source table up to YYYMM
    :type source_table_id_prefix: str
    :param period: Number of days max window for the filter.
    :type period: int
    :param use_legacy_sql: True to use legacy sql
    :type use_legacy_sql: bool
    :param write_disposition: how to write to BQ
    :type write_disposition: str
    :return: None
    :rtype: None
    """
    raw_query = get_query(source_query_path)

    query = create_query(
        source_dataset_id,
        source_table_id_prefix,
        period,
        raw_query
    )

    run_query(
        query,
        project_id,
        target_dataset_id,
        target_table_id,
        use_legacy_sql,
        write_disposition
    )
    logger.info("'{}.{}' DONE.".format(target_dataset_id, target_table_id))


def get_query(query_path):
    """get the query string as saved in sql script.

    :param query_path: Path of the query
    :type query_path: str
    :return: query as loaded from file
    :rtype: str
    """
    logger.info("loading query string from {}".format(query_path))

    with open(query_path, 'r') as f:
        raw_query = f.read()

    return raw_query


def create_query(source_dataset_id,
                 source_table_id_prefix,
                 period,
                 raw_query):
    """Create a sql script for word2vec.

    :param source_dataset_id: name of source dataset
    :type source_dataset_id: str
    :param source_table_id_prefix: name of source table up to YYYYMM
    :type source_table_id_prefix: str
    :param period: Number of days max window for the filter.
    :type period: int
    :param raw_query: query string as loaded from sql file
    :type raw_query: str
    :return: query
    :rtype: str
    """
    logger.info("creating table query string...")
    source_table_enddate = datetime.datetime.now()

    def date_str(date):
        """Create date string from datetime object.

        :param date: datetime date object
        :type date: datetime.datetime
        :return: string representing date in YYYYMM
        :rtype: str
        """
        return "{}{}".format(date.year, '{:02d}'.format(date.month))

    # get a list of all the date strings that fall in the last nr days.
    date_str_list = (
        sorted(list(set(
            [
                date_str(source_table_enddate - datetime.timedelta(i))
                for i in range(period+1)
            ]
        )))
    )

    # create table query list from above date list
    table_query_date_str = ""
    for date_count, date_id in enumerate(date_str_list):
        table_query_date_str += ("table_id = '{}{}'".format(
            source_table_id_prefix,
            date_id
        ))

        # put 'OR's between the table_ids
        if date_count < len(date_str_list) - 1:
            table_query_date_str += " OR "

    table_query_str = 'TABLE_QUERY({}, "{}")'.format(
        source_dataset_id,
        table_query_date_str
    )
    logger.info("table query string:  {}".format(table_query_str))

    query = raw_query.format(table_query_str)

    return query


def run_query(query,
              project_id,
              target_dataset_id,
              target_table_id,
              use_legacy_sql,
              write_disposition):
    """Use Facade to execute query and save result to in BQ.

    :param query: query string
    :type query: str
    :param project_id: name of project
    :type project_id: str
    :param target_dataset_id: name of target dataset
    :type target_dataset_id: str
    :param target_table_id: name of target table
    :type target_table_id: str
    :param use_legacy_sql: True to use legacy sql
    :type use_legacy_sql: bool
    :param write_disposition: how to write to BQ
    :type write_disposition: str
    :return: None
    :rtype: None
    """
    logger.info("running query to '{}.{}'".format(
        target_dataset_id,
        target_table_id
    ))
    if not use_legacy_sql:
        logger.info("NOT using legacy SQL")

    bq_obj = BigQuery(project_id)

    bq_obj.execute_async_query_to_table(
        target_dataset_id,
        target_table_id,
        query,
        use_legacy_sql=use_legacy_sql,
        write_disposition=write_disposition
    )
