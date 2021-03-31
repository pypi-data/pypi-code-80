# -*- coding: UTF-8 -*-

import os
import sqlite3 as sl3


class RealDB(object):
    # region 重写
    def __init__(self, db_info: dict):
        """
        创建一个sqlite访问类实例
        如果创建成功，类的valid属性为True，否则为False
        :param db_info:  sqlite初始化参数
                         一个字典：
                             - 至少应包含 'dbname'：数据库文件名（含路径）
                             - 如果包含 'auto_create'且为True，则会自动创建不存在的数据库文件
        """
        super(RealDB, self).__init__()
        # 参数检查
        self.IsValid = False
        if not isinstance(db_info, dict):
            return
        if 'dbname' not in db_info or not isinstance(db_info['dbname'], str):
            return
        # 标准化数据库文件名
        if not os.path.isabs(db_info['dbname']):
            db_info['dbname'] = os.path.join(os.path.abspath('.'), db_info['dbname'])
        # 检查数据库是否存在
        if not os.path.isfile(db_info['dbname']):
            if os.path.exists(db_info['dbname']):
                # 存在，但不是文件
                return
            if 'auto_create' not in db_info or db_info['auto_create'] not in [True]:
                # 数据库文件不存在，且不自动创建
                return
            # 创建不存在的数据库文件
            # noinspection PyBroadException
            try:
                with sl3.connect(db_info['dbname']):  # 创建数据库
                    pass
                if not os.path.isfile(db_info['dbname']):
                    # 创建数据库文件失败
                    return
            except Exception:
                return
        # 初始化sqlite数据库操作类实体成功
        self.__db_file = db_info['dbname']
        self.IsValid = True
        return
    # endregion

    # region 类静态方法
    @staticmethod
    def __is_valid_table_name(table: str) -> bool:
        """
        判断指定的字符串是否是一个合法的sqlit表名称
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
        if sql[:6] not in ('UPDATE', 'DELETE', 'INSERT'):
            return False
        return True
    # endregion

    # region 属性
    @property
    def valid(self):
        """
        当前sqlite访问类实例是否正常可用
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
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        if not isinstance(fetch_size, int):
            return False, '参数 fetch_size 期望是一个int，但是传入一个 {}'.format(type(fetch_size))
        try:
            with sl3.connect(self.__db_file) as conn:
                executor = conn.execute(sql)
                if 0 == fetch_size:
                    return True, 0
                elif 1 == fetch_size:
                    result = executor.fetchone()
                    return True, result
                elif 0 > fetch_size:
                    result = executor.fetchall()
                    return True, result
                else:
                    result = executor.fetchmany(fetch_size)
                    return True, result
        except Exception as err:
            return False, 'execute <{}> failed: <{}>'.format(sql, err)

    def batch_change(self, sql: str, data: (list, tuple)) -> tuple:
        """
        根据指定的参数，多次执行一种sqlite事务类操作
        :param sql:  slq模板，需要填充参数的地方一律用 ？ 代替，不需要考虑参数的数据类型
        :param data:  模板参数，数据类型要与对应数据列一致
        :return: 执行结果
                   成功  （True， 0）
                   失败  （False，失败信息）
        """
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        if not RealDB.__is_transaction_action(sql):
            return False, '不能对非事务指令执行batch_change: {}'.format(sql)
        try:
            with sl3.connect(self.__db_file) as conn:
                conn.executemany(sql, data)
        except Exception as err:
            return False, '{}'.format(err)
        return True, 0

    def all_tables(self) -> list:
        """
        列出数据库中所有的表
        :return: 存有表名的list，如果没有表则返回[]
        """
        assert self.IsValid, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        run_stat, records = self.exec(f'''{'SELECT'} name FROM sqlite_master WHERE type='table' ''', -1)
        assert run_stat, records
        all_tables = []
        for item in records:
            all_tables.append(item[0])
        return all_tables

    def table_exist(self, table: str) -> tuple:
        """
        检查指定的表是否存在
        :param table:  待检查的表名
        :return:
            存在    (True, 'exist')
            不存在  (False, 不存在/失败原因)
        """
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        if not self.__is_valid_table_name(table):
            return False, '表名 {} 非法'.format(table)
        table = table.strip()
        try:
            with sl3.connect(self.__db_file) as conn:
                sql = f'''{'SELECT'} sql FROM sqlite_master WHERE type='table' AND tbl_name='{{}}' '''
                executor = conn.execute(sql.format(table))
                chk_rlst = executor.fetchall()
                if 0 == len(chk_rlst):
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
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        if not self.__is_valid_table_name(table):
            return True, '表名 {} 非法'.format(table)
        table = table.strip()
        if not self.table_exist(table)[0]:
            return True, '表 {} 不存在'.format(table)
        try:
            with sl3.connect(self.__db_file) as conn:
                sql = f'''{'DROP'} TABLE {{}} '''
                conn.execute(sql.format(table))
        except Exception as err:
            return False, '{}'.format(err)
        if self.table_exist(table)[0]:
            return False, '表 {} 删除失败，仍然存在'.format(table)
        return True, 0

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
        if not self.IsValid:
            return False, '指向 {} 的RealDB当前状态无效'.format(self.__db_file)
        if not isinstance(sqls, (list, tuple)):
            return False, '参数必须是list或tuple，实际上传入了一个{}'.format(type(sqls))
        if pre_check:
            for row in sqls:
                # 检查每一行指令是否合法
                if not isinstance(row, (list, tuple)) or len(row) not in (1, 2):
                    return False, '''指令行结构非法: {}'''.format(row)
                if not RealDB.__is_transaction_action(row[0]):
                    return False, '不能对非事务指令执行事务: {}'.format(row)
                if 2 == len(row) and not isinstance(row[1], (list, tuple)) and len(row[1]) < 1:
                    return False, '指令行参数非法: {}'.format(row)
        # 执行
        try:
            with sl3.connect(self.__db_file, isolation_level=None) as conn:
                conn.execute("BEGIN TRANSACTION")
                empty_param = (tuple(), )
                for row in sqls:
                    conn.executemany(row[0], row[1] if 2 == len(row) else empty_param)
                conn.execute("COMMIT")
        except Exception as err:
            return False, '执行失败：{} @ {}'.format(err, row)
        return True, 0
    # endregion
