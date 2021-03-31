# -*- coding: UTF-8 -*-

from psycopg2.pool import SimpleConnectionPool


class RealDB(object):
    # region 重写
    def __init__(self, db_info: dict):
        """
        创建一个pg数据库访问类实例
        如果创建成功，类的valid属性为True，否则为False
        :param db_info:  pg数据库初始化参数
                         一个字典，至少应包含 'host'、'port'、'user'、'password'、'dbname' 信息
        """
        super(RealDB, self).__init__()
        # 参数检查
        self.IsValid = False
        if not self.__valid_db_info(db_info):
            return
        # 初始化postgres数据库操作类实体
        self.__db_info = db_info
        if 'minconn' not in db_info:
            db_info['minconn'] = 1
        if 'maxconn' not in db_info or db_info['minconn'] >= db_info['maxconn']:
            db_info['maxconn'] = db_info['minconn'] + 1
        self.__pool = SimpleConnectionPool(**db_info)  # 创建连接池
        self.IsValid = True
        return
    # endregion

    # region 类静态方法
    @staticmethod
    def __is_valid_table_name(table: str) -> bool:
        """
        判断指定的字符串是否是一个合法的pg表名称
        :param table:  待判断的字符串
        :return:
            合法  True
            非法  False
        """
        if not isinstance(table, str):
            return False
        table = table.strip()
        if '' == table:
            return False
        return True

    @staticmethod
    def __is_transaction_action(sql: str):
        """
        判断sql字符串是否是一个事务指令
        :param sql:  待判断的sql字符串
        :return:
            是    True
            不是  False
        """
        if not isinstance(sql, str):
            return False
        sql = sql.strip().upper()
        if sql[:6] not in ('UPDATE', 'DELETE', 'INSERT', 'CREATE', 'ALERT ') and sql[:4] != 'DROP':
            return False
        return True

    @staticmethod
    def __valid_db_info(db_info: dict) -> bool:
        """
        数据库连接信息合法性检查
        :param db_info: 数据库连接信息
        :return:
            合法  True
            非法  False
        """
        if not isinstance(db_info, dict):
            return False
        if 'host' not in db_info or not isinstance(db_info['host'], str):
            return False
        if 'port' not in db_info or not isinstance(db_info['port'], str):
            return False
        if 'user' not in db_info or not isinstance(db_info['user'], str):
            return False
        if 'password' not in db_info or not isinstance(db_info['password'], str):
            return False
        if 'dbname' not in db_info or not isinstance(db_info['dbname'], str):
            return False
        if 'minconn' in db_info and (not isinstance(db_info['minconn'], int) or db_info['minconn'] < 1):
            return False
        if 'maxconn' in db_info and (not isinstance(db_info['maxconn'], int) or db_info['maxconn'] < 1):
            return False
        if 'minconn' in db_info and 'maxconn' in db_info and db_info['maxconn'] <= db_info['minconn']:
            return False
        return True
    # endregion

    # region 属性
    @property
    def valid(self):
        """
        当前pg访问类实例是否正常可用
        :return:
            可用    True
            不可用  False
        """
        return self.IsValid
    # endregion

    # region 内部函数
    # endregion

    # region 实例方法
    def exec(self, sql: str, fetch_size: int = 0) -> tuple:
        """
        执行一条sql语句
        :param sql:  待执行语句
        :param fetch_size:  执行结果获取方式
                              0   只获取语句执行成功失败
                              1   只获取第一条查询数据
                              >1  获取fetch_size指定数量的查询数据
                              <0  获取所有查询数据
        :return: 执行结果
                   成功  （True，查询数据）
                   失败  （False，失败信息）
        """
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_info)
        if not isinstance(fetch_size, int):
            return False, '参数 fetch_size 期望是一个int，但是传入一个 {}'.format(type(fetch_size))
        try:
            conn = None
            with self.__pool.getconn() as conn:
                cur = conn.cursor()
                cur.execute(sql)
                if RealDB.__is_transaction_action(sql):
                    conn.commit()
                    fetch_size = 0
                if 0 > fetch_size:
                    result = cur.fetchall()
                    return True, result
                elif 0 == fetch_size:
                    return True, cur.rowcount
                elif 1 == fetch_size:
                    result = cur.fetchone()
                    return True, result
                else:
                    result = cur.fetchmany(fetch_size)
                    return True, result
        except Exception as err:
            return False, 'execute <{}> faild: <{}>'.format(sql, err)
        finally:
            if conn is not None:
                self.__pool.putconn(conn)

    def batch_change(self, sql: str, data: (list, tuple)) -> tuple:
        """
        根据指定的参数，多次执行一种pg事务类操作
        :param sql:  slq模板，需要填充参数的地方一律用 %s 代替，不需要考虑参数的数据类型
        :param data:  模板参数，数据类型要与对应数据列一致
        :return: 执行结果
                   成功  （True， 0）
                   失败  （False，失败信息）
        """
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_info)
        if not RealDB.__is_transaction_action(sql):
            return False, '不能对非事务指令执行batch_change: {}'.format(sql)
        try:
            conn = None
            with self.__pool.getconn() as conn:
                cur = conn.cursor()
                cur.executemany(sql, data)
                effect_rows = cur.rowcount
                conn.commit()
        except Exception as err:
            return False, '{}'.format(err)
        finally:
            if conn is not None:
                self.__pool.putconn(conn)
        return True, effect_rows

    def all_tables(self, schema: str = 'public') -> list:
        """
        列出数据库中所有的表
        :param schema:  查询表所在的schema，默认为 public
        :return: 存有表名的list，如果没有表则返回[]
        """
        assert self.IsValid, '指向 {} 的RealDB当前状态无效'.format(self.__db_info)
        dst_tables = []
        try:
            with self.__pool.getconn() as conn:
                cur = conn.cursor()
                # 查询到指定的schema
                sql = f'''{'SELECT'} oid FROM pg_catalog.pg_namespace WHERE nspname = '{schema}' '''
                cur.execute(sql)
                dst_schema = cur.fetchone()
                assert len(dst_schema) > 0, f'schema {schema} is not exist.'
                dst_oid = dst_schema[0]
                # 在指定的schema中查询表
                sql = f'''{'SELECT'} relname FROM pg_catalog.pg_class WHERE relnamespace = {dst_oid} and reltype <> 0'''
                cur.execute(sql)
                all_tables = cur.fetchall()
                for item in all_tables:
                    dst_tables.append(item[0])
        except Exception as err:
            raise err
        finally:
            if conn is not None:
                self.__pool.putconn(conn)
        return dst_tables

    def table_exist(self, table: str, schema: str = 'public') -> tuple:
        """
        检查指定的表是否存在
        :param table:  待检查的表名
        :param schema:  查询表名所在的schema，默认为 public
        :return:
            存在    (True, 'exist')
            不存在  (False, 'not exist' 或 失败原因)
        """
        if not self.__is_valid_table_name(table):
            return False, '表名 {} 非法'.format(table)
        table = table.strip()
        try:
            all_tables = set(self.all_tables(schema=schema))
            if table not in all_tables:
                return False, 'not exist'
        except Exception as err:
            return False, '{}'.format(err)
        return True, 'exist'

    def rmv_table(self, table: str) -> tuple:
        """
        删除指定的表
        :param table:  待删除的表名
        :return:
            删除成功  True
            删除失败  False
        """
        if not self.__is_valid_table_name(table):
            return True, '表名 {} 非法'.format(table)
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_info)
        table = table.strip()
        if not self.table_exist(table)[0]:
            return True, '表 {} 不存在'.format(table)
        try:
            conn = None
            with self.__pool.getconn() as conn:
                cur = conn.cursor()
                sql = f'''{'DROP'} TABLE {{}} '''
                cur.execute(sql.format(table))
                conn.commit()
        except Exception as err:
            return False, '{}'.format(err)
        finally:
            if conn is not None:
                self.__pool.putconn(conn)
        if self.table_exist(table)[0]:
            return False, '表 {} 删除失败，仍然存在'.format(table)
        return True, 'ok'

    def do_transaction(self, sqls: (list, tuple), pre_check: bool = False) -> tuple:
        """
        作为一个事务，执行一组（可以多种）事务操作
        支持批参数，即其中的一种操作，可以像 batch_change 方法一样被执行多次
        :param sqls:  待执行的一组sql模板，以及他们的参数
        :param pre_check:  执行前是否检查每一条sql事务操作模板的合法性
        :return:  执行结果
                    成功  （True，0）
                    失败  （False，失败原因）
        """
        # 参数检查
        if not isinstance(sqls, (list, tuple)):
            return False, '参数必须是list或tuple，实际上传入了一个{}'.format(type(sqls))
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_info)
        if pre_check:
            for row in sqls:
                # 检查每一行指令是否合法
                if not isinstance(row, (list, tuple)) or len(row) < 1 or len(row) > 2:
                    return False, '''指令行结构非法: {}'''.format(row)
                if 2 == len(row) and not isinstance(row[1], (list, tuple)) and len(row[1]) < 1:
                    return False, '指令行参数非法: {}'.format(row)
                if not RealDB.__is_transaction_action(row[0]):
                    return False, '不能对非事务指令执行事务: {}'.format(row)
        # 执行
        effect_rows = 0
        try:
            conn = None
            with self.__pool.getconn() as conn:
                cur = conn.cursor()
                empty_param = (tuple(), )
                for row in sqls:
                    cur.executemany(row[0], row[1] if 2 == len(row) else empty_param)
                    effect_rows += cur.rowcount
                conn.commit()
        except Exception as err:
            return False, '执行失败：{} @ {}'.format(err, row)
        finally:
            if conn is not None:
                self.__pool.putconn(conn)
        return True, effect_rows
    # endregion
