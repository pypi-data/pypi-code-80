# -*- coding: UTF-8 -*-

import os
import sqlite3 as sl3
from RealToolkits import find_one_in_path, valid_fn
import json
from .node import RealCfgNode


class RealCfg(object):
    # region 重写
    def __init__(self, cfg_name: str):
        super(RealCfg, self).__init__()
        # 检查配置器名称是否合法
        self.__IsValid = False
        self.LastErr = ''
        if not isinstance(cfg_name, str):
            self.LastErr = '期望指定的配置器名称是一个str，实际上是{}'.format(type(cfg_name))
            return
        cfg_name = cfg_name.strip()
        if not valid_fn(cfg_name):
            self.LastErr = '指定的配置器名称 <{}> 无法作为一个配置数据库文件的合法文件名'.format(cfg_name)
            return
        # 记录配置器名称
        self.__cfg_name = cfg_name
        # 确保db文件可用
        curr_path = os.path.abspath('.')
        db_fn = cfg_name + '.db'
        find_result = find_one_in_path(curr_path, db_fn, find_folder=False)
        if 0 == len(find_result):
            # db文件当前不存在
            # 在进程所在路径新建数据库
            db_full_name = os.path.join(curr_path, db_fn)
            if not self.create_new_cfg_db(db_full_name):
                self.LastErr = '无法创建配置数据库 {}'.format(db_full_name)
                return
            self.__db_file = db_full_name
        else:
            # db文件已经存在，检查是否具备了必要的表
            db_path = list(find_result[db_fn].keys())[0]
            full_db_name = os.path.join(db_path, db_fn)
            if not self.is_valid_db_file(full_db_name):
                self.LastErr = '已经存在数据库文件 {} ，但不合法或已经损坏'.format(full_db_name)
                return
            # 文件合法，记录文件路径，将使用此文件作为此cfg实例的数据库存储
            self.__db_file = full_db_name
        # 配置器可以正常使用
        self.__IsValid = True
        return
    # endregion

    # region 类静态方法
    @staticmethod
    def create_new_cfg_db(full_db_name: str) -> bool:
        """
        用指定的路径和文件名称创建一个新的RealCfg数据库
        :param full_db_name: 数据库文件绝对路径
        :return:
            成功  True
            失败  False
        """
        # 参数检查
        if not isinstance(full_db_name, str):
            return False
        if not os.path.isabs(full_db_name):
            return False
        if os.path.exists(full_db_name):
            return False
        # 创建数据库和表
        # noinspection PyBroadException
        try:
            with sl3.connect(full_db_name) as conn:  # 创建数据库
                if not RealCfg.create_new_cfg_tables(conn):  # 创建表
                    return False
        except Exception:
            return False
        return True

    @staticmethod
    def create_new_cfg_tables(conn: sl3.Connection) -> bool:
        """
        用给定的连接创建cfg实体所需的表
        :param conn: 外部传入的数据库连接
        :return:
            创建成功  True
            创建失败  False
        """
        if not isinstance(conn, sl3.Connection):
            return False
        create_tbl_sql = f'''{'CREATE'} TABLE cfg_data
                            (
                                idx TEXT NOT NULL constraint cfg_data_pk PRIMARY KEY ,
                                cfg_key TEXT NOT NULL ,
                                cfg_value TEXT NOT NULL ,
                                value_type TEXT NOT NULL ,
                                key_level INTEGER NOT NULL ,
                                father_idx TEXT NOT NULL,
                                father_path TEXT NOT NULL
                            )'''  # 建表脚本
        # noinspection PyBroadException
        try:
            cur = conn.cursor()
            cur.execute(create_tbl_sql)
            conn.commit()  # 用别人给的connection，做完操作及时commit是个好习惯
        except Exception as err:
            print(err)
            return False
        return True

    @staticmethod
    def is_valid_db_file(full_db_name: str) -> bool:
        """
        检查指定的文件是否是合法的cfg数据库文件
        :param full_db_name: 待判断的文件，如果文件不存在，视同不合法
        :return:
            合法   True
            不合法 False
        """
        # 参数检查
        # noinspection PyBroadException
        try:
            if not os.path.isfile(full_db_name):
                return False
        except Exception:
            return False
        # 检查数据库是否包含必须的表
        tbl_chk_sql = f''' {'SELECT'} sql FROM sqlite_master WHERE type='table' AND tbl_name='cfg_data' '''
        # noinspection PyBroadException
        try:
            with sl3.connect(full_db_name) as tmp_conn:
                chk_cur = tmp_conn.cursor()
                chk_search = chk_cur.execute(tbl_chk_sql)
                chk_rlst = chk_search.fetchall()
                if 0 == len(chk_rlst):
                    return False
                # TODO: 后面这里可以继续加上对查询结果（建表脚本）的解析，判断字段是否合法
        except Exception:
            return False
        return True

    @staticmethod
    def value_to_sql_expression(origin_value) -> str:
        """
        生成一个节点（配置项）值在sql语句中的字符串表达形式
        :param origin_value: 待转换的值
        :return: 可以直接嵌入SQL语句的字符串
        """
        node_type = RealCfgNode.value_to_node_type(origin_value)
        storage = RealCfgNode.value_to_storage(origin_value)
        if storage is None or node_type is None:
            raise ValueError('value_to_sql_expression: type {} is not supported'.format(type(origin_value)))
        return RealCfg.sql_value_fix(storage)

    @staticmethod
    def sql_value_fix(v: str) -> str:
        """
        确保嵌入sql语句的值符合sql语法
        :param v: 将被嵌入sql语句的值
        :return: 可以直接嵌入SQL语句的字符串
        """
        return "'" + v.replace("'", "''") + "'"
    # endregion

    # region 实例内部函数
    def __select_node_data(self, *args, idx: (str, type(None)) = None) -> (tuple, type(None)):
        if 0 < len(args):
            # 路径参数比idx参数优先
            node_idx = RealCfgNode.generate_node_idx(*args)
            if node_idx is None:
                return None
        elif isinstance(idx, str) and 32 == len(idx.strip()):
            node_idx = idx.strip()
        else:
            return None
        node_idx = RealCfg.sql_value_fix(node_idx)
        qry_sql  = f'''{'SELECT'} {{}} FROM cfg_data WHERE idx={{}} '''
        fields   = '''idx, cfg_key, cfg_value, value_type, key_level, father_idx , father_path'''
        qry_sql  = qry_sql.format(fields, node_idx)
        try:
            with sl3.connect(self.db_file) as conn:
                qry_rlst = conn.execute(qry_sql.format(node_idx))
                node_data = qry_rlst.fetchone()
                if node_data is None:
                    return None
        except Exception as err:
            self.LastErr = str(err)
            return None
        return node_data

    def __select_sub_nodes_data(self, *args, idx: (str, type(None)) = None) -> list:
        qry_sql = f'''{'SELECT'} idx,cfg_key,cfg_value,value_type,key_level,father_idx,father_path FROM cfg_data'''
        if 0 == len(args) and idx is None:
            qry_sql += ''' WHERE key_level=1'''
        else:
            if 0 < len(args):
                # 路径参数比idx参数优先
                curr_item_data = self.__select_node_data(*args)
                if curr_item_data is None:
                    return []
                curr_item_idx = curr_item_data[0]
            elif isinstance(idx, str) and 32 == len(idx.strip()):
                curr_item_idx = idx.strip()
            else:
                return []
            qry_sql += ''' WHERE father_idx={}'''.format(RealCfg.sql_value_fix(curr_item_idx))
        try:
            with sl3.connect(self.db_file) as conn:
                qry_rlst = conn.execute(qry_sql)
                sub_nodes_data = qry_rlst.fetchall()
        except Exception as err:
            self.LastErr = str(err)
            return []
        return sub_nodes_data

    def __pkg_nodes_data(self, nodes_data: list) -> list:
        # idx, cfg_key, cfg_value, value_type, key_level, father_idx , father_path
        nodes = []
        for node_data in nodes_data:
            node_value = json.loads(node_data[2])
            curr_node = RealCfgNode(node_data[1], node_value, node_data[3], node_data[6])
            if curr_node is None:
                self.LastErr = 'node data {} 无法生成RealCfgNode'.format(curr_node)
                continue
            nodes.append(curr_node)
        return nodes
    # endregion

    # region 实例属性
    @property
    def is_valid(self):
        return self.__IsValid

    @property
    def name(self):
        return self.__cfg_name

    @property
    def db_file(self):
        return self.__db_file
    # endregion

    # region 实例方法
    def sub_nodes_by_path(self, *args) -> list:
        """
        根据指定的节点（配置项）路径，查询该路径下一层的所有node
        如果指定的路径不存在，返回[]
        :param args: 节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key，如果不提供则获取所有第一层节点
        :return: 包含路径下每一个直接子节点（配置项）的list
        """
        args = [sec.strip() for sec in args]
        # 获取指定路径所有直接子节点的信息
        nodes_data = self.__select_sub_nodes_data(*args)
        # 打包每个子节点信息到RealCfgNode
        return self.__pkg_nodes_data(nodes_data)

    def sub_nodes_by_idx(self, idx: (str, type(None)) = None) -> list:
        """
        根据指定的节点（配置项）idx，查询隶属与该节点（配置项）的所有直接子节点（配置项）
        如果指定的idx不存在，返回[]
        如果参数idx为None（默认值），则获取所有第一层节点
        :param idx: 节点（配置项）idx，可以为None
        :return: 包含idx对应节点下每一个直接子节点（配置项）的list
        """
        # 获取指定路径所有直接子节点的信息
        nodes_data = self.__select_sub_nodes_data(idx=idx)
        # 打包每个子节点信息到RealCfgNode
        return self.__pkg_nodes_data(nodes_data)

    def get_node_by_path(self, *args) -> (RealCfgNode, type(None)):
        """
        根据指定的节点（配置项）路径，获取该节点
        :param args: 节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key
        :return: 指定的节点（RealCfgNode），不存在时返回None
        """
        args = [sec.strip() for sec in args]
        node_data = self.__select_node_data(*args)
        if node_data is None:
            return None
        nodes_but_just_one = self.__pkg_nodes_data([node_data])
        if 0 == len(nodes_but_just_one):
            return None
        return nodes_but_just_one[0]

    def get_node_by_idx(self, idx: str) -> (RealCfgNode, type(None)):
        """
        根据指定的节点（配置项）idx，获取该节点
        :param idx: 节点（配置项）idx
        :return: 指定的节点（RealCfgNode），失败或不存在时返回None
        """
        if not isinstance(idx, str) or 32 != len(idx.strip()):
            return None
        node_data = self.__select_node_data(idx=idx)
        if node_data is None:
            return None
        nodes_but_just_one = self.__pkg_nodes_data([node_data])
        if 0 == len(nodes_but_just_one):
            return None
        return nodes_but_just_one[0]

    def set_node(self,
                 new_value: (int, float, bool, str, list, set, tuple, dict),
                 *args) -> bool:
        """
        设置指定的节点（配置项）的值：
            > 当指定节点（配置项）的父节点不存在时，返回失败
            > 如果指定的节点（配置项）已经存在，则修改其值
            > 如果指定的节点（配置项）不存在，则创建对应的节点（配置项）
            > 当设定的值为None时：
                - 如果节点已经存在，只把节点值改为null
                - 如果节点不存在，创建一个节点类型为str，值为null的新节点
        :param new_value: 节点的值
        :param args: 节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key
        :return:
            成功 True
            失败 False
        """
        # 参数检查
        args = [sec.strip() for sec in args]
        if not RealCfgNode.is_valid_node_path(*args):
            self.LastErr = 'set_node: try to set a node with invalid path <{}>'.format(args)
            return False
        node_path_len = len(args)
        if 0 == node_path_len:
            # 未指定路径
            self.LastErr = 'set_node: try to set a node without path'
            return False
        if 1 < node_path_len and self.__select_node_data(*args[:-1]) is None:
            # 父节点不存在
            self.LastErr = 'set_node: try to set a node <{}> but father node not exist'.format(args)
            return False
        # 如果节点值是容器，需要先进行标准化
        # noinspection PyBroadException
        try:
            if isinstance(new_value, (list, set, tuple)):
                new_value = RealCfgNode.to_std_json_list(new_value)
            elif isinstance(new_value, dict):
                new_value = RealCfgNode.to_std_json_dict(new_value)
        except Exception:
            self.LastErr = 'set_node: value <{}> can not be changed to a std json container'.format(new_value)
            return False
        # 判断节点是否存在
        already_exist = False if self.__select_node_data(*args) is None else True
        # 生成insert/update语句所需的sql片段
        sec_idx    = RealCfgNode.generate_node_idx(*args)
        sec_idx    = RealCfg.sql_value_fix(sec_idx)
        sec_key    = RealCfg.sql_value_fix(args[-1])
        sec_value  = RealCfg.value_to_sql_expression(new_value)
        sec_level  = node_path_len
        sec_father = RealCfgNode.to_std_node_path(*args[:-1])
        sec_father = RealCfg.sql_value_fix(sec_father)
        sec_f_idx  = RealCfgNode.generate_node_idx(*args[:-1])
        sec_f_idx  = RealCfg.sql_value_fix(sec_f_idx)
        sec_type   = RealCfg.sql_value_fix(RealCfgNode.value_to_node_type(new_value))
        if sec_value is None:
            # 指定要写入节点（配置项）的值非法
            self.LastErr = 'set_node: invalid value <{}>'.format(new_value)
            return False
        # 生成SQL语句
        if already_exist:
            if new_value is None:
                sql_temp = f'''{'UPDATE'}  cfg_data SET cfg_value={{}} WHERE idx={{}} '''
                sql_str = sql_temp.format(sec_value, sec_idx)
            else:
                sql_temp = f'''{'UPDATE'} cfg_data SET cfg_value={{}}, value_type={{}} WHERE idx={{}} '''
                sql_str = sql_temp.format(sec_value, sec_type, sec_idx)
        else:
            sql_temp = f'''{'INSERT'} INTO cfg_data VALUES ({{}}, {{}}, {{}}, {{}}, {{}}, {{}}, {{}}) '''
            sql_str = sql_temp.format(sec_idx, sec_key, sec_value, sec_type, sec_level, sec_f_idx, sec_father)
        try:
            with sl3.connect(self.db_file) as conn:
                conn.execute(sql_str)
        except Exception as err:
            self.LastErr = 'set_node: sql <{}> executed faild <{}>'.format(sql_str, err)
            return False
        return True

    def rmv_node_by_path(self, *args) -> bool:
        """
        删除指定节点
        :param args: 节点路径
        :return:
            True   删除成功、节点不存在
            False  删除失败、路径非法
        """
        if 0 == len(args):
            return True
        idx = RealCfgNode.generate_node_idx(*args)
        if idx is None:
            return True
        return self.rmv_node_by_idx(idx=idx)

    def rmv_node_by_idx(self, idx: str) -> bool:
        node_will_be_rmv = self.get_node_by_idx(idx)
        if node_will_be_rmv is None:
            # 节点本来就不存在
            return True
        # 如果节点存在，先检查它有没有子节点
        # 有的话要先删除子节点
        child_nodes = self.sub_nodes_by_idx(idx)
        for each_child in child_nodes:
            self.rmv_node_by_idx(each_child.idx)
        # 到这里，可以确认此节点（配置项）不存在子节点（配置项）了
        # 删除此节点
        sql_str = f'''{'DELETE'} FROM  cfg_data WHERE idx= {RealCfg.sql_value_fix(idx)}'''
        try:
            with sl3.connect(self.db_file) as conn:
                conn.execute(sql_str)
        except Exception as err:
            self.LastErr = 'rmv_node: sql <{}> executed faild <{}>'.format(sql_str, err)
            return False
        return True

    def rmv_all_nodes(self) -> bool:
        """
        清空所有配置项
        :return:
            成功  True
            失败  False
        """
        sql_str = f'''{'DELETE'} FROM  cfg_data'''
        try:
            with sl3.connect(self.db_file, isolation_level=None) as conn:
                conn.execute("BEGIN TRANSACTION")
                conn.execute(sql_str)
                conn.execute("COMMIT")
        except Exception as err:
            self.LastErr = 'rmv_all_nodes faild: {}'.format(err)
            return False
        return True

    # region
