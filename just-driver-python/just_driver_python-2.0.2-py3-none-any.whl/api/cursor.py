from .connection import Connection
from .errors import InterfaceError, ProgrammingError, NotSupportedError, DataError, JustConnectionError
from ..constant.request_enum import RequestEnum
from ..log import logger


class Frame(object):

    def __init__(self, offset: int, done: bool, rows: list):
        self.done = done
        self.offset = offset
        self.rows = rows


class Cursor(object):
    """
    Cursor对象，负责操作数据
    """

    class States(object):
        (
            NONE,
            RUNNING,
            FINISHED,
            CLOSED
        ) = range(4)

    _states = States()

    def __init__(self, conn: Connection):
        self._conn = conn
        self._current_statement_id = None
        self._state = self._states.NONE
        self._reset_state()

        self.page_size = conn.conn_config.page_size
        self._frame: Frame = Frame(0, False, [])
        self._acc_offset = -1
        self._acc_total = 0
        self._index = -1

        super(Cursor, self).__init__()

    @property
    def description(self):
        return None

    @property
    def rowcount(self):
        return self._rowcount

    def close(self):
        """
        关闭后不再可用，否则抛出Error
        """
        # TODO 关闭client连接
        self._state = self._states.CLOSED
        close_statement_request = {
            "request": RequestEnum.CLOSE_STATEMENT.value,
            "statementId": self._current_statement_id
        }
        self._conn.service.request(close_statement_request)

    def execute(self, operation: str):
        """
        准备和执行数据库操作（查询或命令）
        参数和操作的映射应该是对应的，参考paramstyle
        这个操作的引用被游标保留，如果同样的操作多次使用，那么可以重复使用
        为了最大化的重用操作，最好使用 .setinputsizes() 来事先指定参数类型和大小。
        参数同样可以是tuple列表。例如，插入很多行数据，但是这种用户被淘汰了，使用 .executemany()方法
        :param operation: 查询语句
        :return: None
        """
        self._check_cursor_closed()
        self._begin_query()

        for i in range(self._conn.conn_config.max_retries):
            try:
                # 1.创建Statement
                create_statement_request = {
                    "request": RequestEnum.CREATE_STATEMENT.value,
                    "connectionId": self._conn.conn_config.connection_id
                }
                create_statement_result = self._conn.service.request(create_statement_request)
                statement_id = create_statement_result['statementId']
                self._current_statement_id = statement_id

                # 2.执行SQL
                prepare_and_execute_request = {
                    "request": RequestEnum.PREPARE_AND_EXECUTE.value,
                    "connectionId": self._conn.conn_config.connection_id,
                    "statementId": statement_id,
                    "sql": operation,
                    "maxRowsInFirstFrame": -1,
                    "maxRowCount": -1
                }
                pe_res = self._conn.service.request(prepare_and_execute_request)
                logger.info('res={}'.format(pe_res))
                if pe_res.get("results") and len(pe_res["results"]) > 0:
                    res = pe_res['results'][0]
                    if res.get('firstFrame'):
                        self._frame = Frame(res["firstFrame"]['offset'], res["firstFrame"]['done'],
                                            res["firstFrame"]['rows'])
                    else:
                        self._frame = Frame(0, False, [])
                    break
                else:
                    raise DataError('results should exists:{}'.format(pe_res))
            except JustConnectionError:
                i += 1
                # re choose uri
                self._conn.open_connection()
                logger.warning('just create statement and execute retry {}'.format(i))
        self._acc_total = len(self._frame.rows)
        self._acc_offset = -1
        self._index = -1
        self._end_query()

    def executemany(self, operation, seq_of_parameters):
        """
        等价于execute的批量请求
        :param operation: 查询语句
        :param seq_of_parameters: 查询语句参数
        :return: None
        """
        raise NotSupportedError("not supported executemany now")

    def fetchone(self):
        """
        :return: 获取查询结果集的下一行数据，返回一个序列或者没有数据时返回None
        """
        self._check_cursor_closed()
        if self._acc_offset < self._acc_total - 1:
            self._acc_offset += 1
            self._index += 1
            return self._frame.rows[self._index]
        if self._frame.done:
            return None
        else:
            fetch_one_request = {
                "request": RequestEnum.FETCH.value,
                "connectionId": self._conn.conn_config.connection_id,
                "statementId": self._current_statement_id,
                "offset": self._acc_offset,
                "fetchMaxRowCount": self.page_size
            }
            res = self._conn.service.request(fetch_one_request)
            if not res['frame'] or len(res['frame']['rows']) == 0:
                self._frame.done = True
                return None
            self._frame = Frame(res['frame']['offset'], res['frame']['done'], res['frame']['rows'])
            self._acc_total += len(self._frame.rows)
            self._acc_offset += 1
            self._index = 0
            # logger.debug("fetch one frame ok: frame.size=%s,current=%s,total=%s")
            return self._frame.rows[self._index]

    def fetchmany(self, size=None):
        """
        返回结果集的下一批数据，返回序列的列表（例如：tuple list）。当没有数据时返回空序列
        参数size可以指定返回的条数，如果没有给定，就是游标的数组长度
        :param size: 期望返回的行数
        :return:
        """
        # 没指定就是剩下这一批的数据量
        if not size:
            size = self._acc_total - self._acc_offset
        all_rows = []
        cnt = 0
        while cnt <= size:
            row = self.fetchone()
            if not row:
                return all_rows
            all_rows.append(row)
        return all_rows

    def fetchall(self):
        """
        :return: 获取所有（剩余的）行数结果集
        """
        row = self.fetchone()
        all_rows = []
        while row:
            all_rows.append(row)
            row = self.fetchone()
        return all_rows

    def setinputsizes(self, sizes):
        # Do nothing.
        pass

    def setoutputsize(self, size, column=None):
        # Do nothing.
        pass

    def _reset_state(self):
        self._state = self._states.NONE

        self._columns = None
        self._types = None
        self._rows = None
        self._rowcount = -1

    def _begin_query(self):
        self._state = self._states.RUNNING

    def _end_query(self):
        self._state = self._states.FINISHED

    def _check_cursor_closed(self):
        if self._state == self._states.CLOSED:
            raise InterfaceError('cursor already closed')

    def _check_cursor_started(self):
        if self._state == self._states.NONE:
            raise ProgrammingError('no results to fetch')
