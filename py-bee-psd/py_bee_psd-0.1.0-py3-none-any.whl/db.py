import contextlib
import logging
from datetime import datetime

from bee_util.data.map import Map
from bee_psd.clause import SelectClause
from bee_psd.column import new_columns, ColumnFilter, Columns
from bee_psd.connection.connection import IConnection
from bee_psd.connection.mysql import MysqlConnection
from bee_psd.delete import DeleteContext, DeleteInfo
from bee_psd.insert import InsertContext, InsertInfo
from bee_psd.select import SelectInfo, SelectContext
from bee_psd.update import UpdateContext, UpdateInfo
from bee_util.errors.error import BeeError

# logging.basicConfig(level=logging.DEBUG)


class DBOptions(Map):

    def __init__(self, name: str = None, provider: str = "mysql"
                 # , address: str=""
                 , max_open_conns: int = 100, max_idle_conns: int = 5
                 , trace=Map(), options=Map()):
        self.name = name
        self.provider = provider
        # self.address = address
        self.max_open_conns = max_open_conns
        self.max_idle_conns = max_idle_conns
        # self.conn_lifetime = conn_lifetime,
        self.trace = trace
        self.options = options
        self.host = "127.0.0.1"
        self.port = 3306
        self.database = "test"
        self.user = "root"
        self.password = "000000"
        self.charset = "utf8mb4"


class DB():
    """
    database's CURD include both simple-sql(Insert,Update,Delete,Select) and orm(Create,Modify,Remove) styles.
    """

    # name = "DB"

    def insert(self, table: str):
        pass

    def update(self, table: str):
        pass

    def delete(self, table: str):
        pass

    def select(self, *cols: str):
        pass

    def save(self, model, *filters: ColumnFilter):
        pass

    def modify(self, model, *filters: ColumnFilter):
        pass

    def remove(self, model):
        pass

    def query(self, cols: Columns, *distinct):
        pass


def trace(func):
    def wrapper(*args, **kw):
        self = args[0]
        enabled = False
        if self.opts.trace["enabled"] != None and self.opts.trace["enabled"] == True:
            enabled = True

        begin = datetime.now().timestamp()
        if enabled:
            logging.debug('psd > call %s()' % func.__name__)
        result = func(*args, **kw)
        end = datetime.now().timestamp()
        if enabled:
            logging.debug('psd > sql: %s, args: %s(%s), time: %s', args[1], args[2], str(len(args[2])), str(end - begin))
        return result

    return wrapper


class Database(DB):
    name = "Database"

    def __init__(self, name="default", opts=DBOptions(), conn=IConnection(), provider=None, stmts={}):
        # def __init__(self, name="default", opts=Options(), conn=None):
        self.name = name
        self.opts = opts
        self.conn = conn
        self.p = provider
        self.stmts = stmts

    def name(self):
        return self.opts.name

    @trace
    def exec(self, query, args=[]):
        return self.conn.exec(query, args)

    @trace
    def find_one(self, query, args=[]):
        return self.conn.find_one(query, args)

    @trace
    def find_list(self, query, args=[]):
        return self.conn.find_list(query, args)

    def insert(self, table) -> InsertContext:
        info = InsertInfo(table=table)
        context = InsertContext(info=info, db=self)
        context.db = self
        context.insert(table)
        return context

    def update(self, table) -> UpdateContext:
        info = UpdateInfo(table=table)
        context = UpdateContext(info=info, db=self)
        context.db = self
        context.update(table)
        return context

    def delete(self, table) -> DeleteContext:
        info = DeleteInfo(table=table)
        context = DeleteContext(info=info, db=self)
        context.db = self
        context.delete(table)
        return context

    def select(self, *cols) -> SelectContext:
        _len = len(cols)
        if _len == 1 and isinstance(cols[0], Columns):
            info = SelectInfo(columns=cols[0])
        else:
            info = SelectInfo(columns=new_columns(*cols))
        context = SelectContext(info=info, db=self)
        context.db = self
        return context

    def save(self, model, *filters: ColumnFilter):
        info = InsertInfo(table=None)
        context = InsertContext(info=info, db=self)
        context.db = self
        return context.save(model, *filters)

    def modify(self, model, *filters: ColumnFilter):
        info = UpdateInfo(table=None)
        context = UpdateContext(info=info, db=self)
        context.db = self
        return context.modify(model, *filters)

    def remove(self, model):
        info = DeleteInfo(table=None)
        context = DeleteContext(info=info, db=self)
        context.db = self
        return context.remove(model)

    def query(self, cols: Columns, *distinct: bool) -> "SelectClause":
        info = SelectInfo(columns=[])
        context = SelectContext(info=info, db=self)
        context.db = self
        return context.select(cols, *distinct)

    def _new_conn(self) -> IConnection:
        if self.opts.provider == "mysql":
            conn = MysqlConnection(host=self.opts.host, port=self.opts.port
                                       , user=self.opts.user, password=self.opts.password, database=self.opts.database, charset=self.opts.charset)
            self.conn = conn
        elif self.opts.provider == "mssql":
            pass
        elif self.opts.provider == "sqlite":
            pass
        return conn

    @contextlib.contextmanager
    def connection(self):

        conn = self._new_conn()
        try:
            yield conn
        except BeeError as e:
            yield None
        finally:
            conn.close()
            del conn

    @contextlib.contextmanager
    def transaction(self):

        conn = self._new_conn()
        conn.begin()
        try:
            yield
        except BaseException as e:
            if conn != None:
                conn.rollback()
                raise e
        finally:
            if conn != None:
                conn.commit()
                conn.close()

