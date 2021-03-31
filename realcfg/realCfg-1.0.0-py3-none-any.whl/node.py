# -*- coding: UTF-8 -*-

import json
import hashlib


class RealCfgNode(object):
    """
    配置器的配置节点，一个节点就是一个配置项
    节点可以有：
        > 父节点（父配置项）
        > 子节点（子配置项）
        > 节点（配置项）自身的值
    节点的值支持如下类型：
        > 数字（int、float）
        > 字符串（str）
        > 布尔值（bool）
        > 数组（list）
        > 字典（dict）
        初始化时，可以传入对应类型的值，也可以传入能够转化成这些类型的值
    """
    # region 重写
    def __new__(cls,
                node_key: str,
                node_value,
                node_type: str,
                node_father: (list, tuple, str, type(None))):
        # 参数检查&整理
        if not isinstance(node_key, str):
            # key类型不合法
            return None
        # noinspection PyBroadException
        try:
            # 检查值与类型是否匹配
            node_type = node_type.lower().strip()
            if 'str' == node_type and node_value is not None:
                if not isinstance(node_value, str):
                    return None
            elif 'int' == node_type and node_value is not None:
                node_value = int(node_value)
            elif 'float' == node_type and node_value is not None:
                node_value = float(node_value)
            elif 'bool' == node_type and node_value is not None:
                if not isinstance(node_value, bool):
                    return None
            elif 'list' == node_type and node_value is not None:
                node_value = RealCfgNode.to_std_json_list(node_value)
            elif 'dict' == node_type and node_value is not None:
                node_value = RealCfgNode.to_std_json_dict(node_value)
        except Exception:
            return None
        if not isinstance(node_father, (list, tuple, str, type(None))):
            # father类型不合法
            return None
        if node_father is None or '/' == node_father:
            father_list = []
        elif isinstance(node_father, str):
            node_father = node_father.strip()
            if '//' in node_father or '' == node_father:
                # father内容不合法
                return None
            if '/' == node_father[0]:
                node_father = node_father[1:]
            father_list = node_father.split('/')
            father_list = [sec.strip() for sec in father_list]
        else:
            # list、tuple类型的father直接赋给father_list
            father_list = node_father
        full_path_list = father_list + [node_key.strip()]
        if not RealCfgNode.is_valid_node_path(*full_path_list):
            # 全路径（含 father 和 key）内容不合法
            return None
        node_level = len(full_path_list)
        # 实例化
        be_self = super(RealCfgNode, cls).__new__(cls)
        be_self.__key = full_path_list[-1]
        be_self.__value = node_value
        be_self.__type = node_type
        be_self.__level = node_level
        be_self.__father = father_list
        be_self.__full_key = full_path_list
        return be_self

    def __init__(self,
                 node_key: str,
                 node_value,
                 node_type: str,
                 node_father: (str, tuple, list, type(None))):
        super(RealCfgNode, self).__init__()
        self.__key_o = node_key
        self.__value_o = node_value
        self.__type_o = node_type
        self.__father_o = node_father
        return

    def __str__(self):
        return '{}: {} <{}>, (level={}, idx={}, father={}, father_idx={})'.format(self.key,
                                                                                  self.value,
                                                                                  self.type,
                                                                                  self.level,
                                                                                  self.idx,
                                                                                  self.father,
                                                                                  self.father_idx)
    # endregion

    # region 类静态方法
    @staticmethod
    def is_valid_node_path(*args) -> bool:
        """
        检查指定的节点（配置项）路径是否是合法路径（不保证实际上存在）
        当没提供任何参数时，函数返回True，视作"代表全体配置数据的第0层"
        :param args: 待检查的节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key
        :return:
            合法   True
            不合法 False
        """
        for arg in args:
            # 要求路径的每一节：
            #     > 必须是字符串
            #     > 去除两端空格后不能是空串
            #     > 不能含有斜杠 '/'
            if not isinstance(arg, str) or '' == arg.strip() or '/' in arg:
                return False
        return True

    @staticmethod
    def to_std_node_path(*args) -> (str, type(None)):
        """
        将给定的节点（配置项）路径，转换成对应的路径字符串
        :param args: 待转换的节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key
        :return:
            成功  各级路径以'/'拼接成的字符串
            失败  None
        """
        args = [sec.strip() for sec in args]
        if not RealCfgNode.is_valid_node_path(*args):
            return None
        the_path = '/'
        if 0 == len(args):
            return the_path
        return the_path + '/'.join(sec.strip() for sec in args)

    @staticmethod
    def generate_node_idx(*args) -> (str, type(None)):
        """
        生成给定的节点（配置项）路径的哈希值
        这里用的是MD5
        这个值将被作为存储到数据库的主键
        如果不指定路径，则判定为生成第0层的idx，将强制使用'/'计算哈希值
        :param args: 节点（配置项）路径，从第1层开始，顺序给出每一层配置项的key
        :return:
            成功  全路径的哈希值
            失败  None（路径非法）
        """
        args = [sec.strip() for sec in args]
        node_path = RealCfgNode.to_std_node_path(*args)
        if node_path is None:
            return None
        the_md5_value = hashlib.md5(node_path.encode('utf8'))
        return the_md5_value.hexdigest()

    @staticmethod
    def to_std_json_list(v) -> list:
        """
        尝试将一个对象转换为符合Json格式要求的list
        无法转换时抛出异常 TypeError
        包含Json不允许的数据类型时，抛出异常 TypeError
        对象包含多层结构时，递归到层次尽头
        :param v: 待转换对象
        :return:
            转换成功  list
            转换失败  抛出异常
        """
        if isinstance(v, (tuple, set)):
            v = list(v)
        if not isinstance(v, list):
            raise TypeError('Type: list is expected, but <{}> found'.format(type(v)))
        idx = -1
        for item in v:
            idx += 1
            if item is None or isinstance(item, (int, float, str, bool)):
                continue
            elif isinstance(item, dict):
                v[idx] = RealCfgNode.to_std_json_dict(item)
            elif isinstance(item, (list, tuple, set)):
                v[idx] = RealCfgNode.to_std_json_list(item)
            else:
                raise TypeError('TypeError: a <{}> is not allowed in json list'.format(type(item)))
        return v

    @staticmethod
    def to_std_json_dict(v) -> dict:
        """
        尝试将一个对象转换为符合Json格式要求的dict
        无法转换时抛出异常 TypeError
        包含Json不允许的数据类型时，抛出异常 TypeError
        对象包含多层结构时，递归到层次尽头
        :param v: 待转换对象
        :return:
            转换成功  dict
            转换失败  抛出异常
        """
        if not isinstance(v, dict):
            raise TypeError('TypeError: dict is expected, but <{}> found'.format(type(v)))
        for k in v:
            item = v[k]
            if item is None or isinstance(item, (int, float, str, bool)):
                continue
            elif isinstance(item, dict):
                v[k] = RealCfgNode.to_std_json_dict(item)
            elif isinstance(item, (list, tuple, set)):
                v[k] = RealCfgNode.to_std_json_list(item)
            else:
                raise TypeError('TypeError: a <{}> is not allowed in json dict'.format(type(item)))
        return v

    @staticmethod
    def storage_to_value(s: str) -> (int, float, str, bool, list, dict, type(None)):
        if not isinstance(s, str):
            raise ValueError('ValueError:  storage_to_value expect a <str> param, but a <{}> instead'.format(type(s)))
        cloth_str = '{{"a":{}}}'.format(s)
        # noinspection PyBroadException
        try:
            value_container = json.loads(cloth_str)
        except Exception:
            return None
        return value_container['a']

    @staticmethod
    def value_to_storage(v: (int, float, str, bool, list, tuple, set, dict, type(None))) -> (str, type(None)):
        # noinspection PyBroadException
        try:
            if v is None:
                return 'null'
            if isinstance(v, str):
                json_str = v.replace('"', r'\"')
                return '"{}"'.format(json_str)
            if isinstance(v, bool):
                # 必须把bool判断放在int判断前面
                # 因为：
                #     isinstance(True, int)、isinstance(False, int) 会返回 True
                #     但 isinstance(一个int值, bool) 并不会
                return 'true' if v else 'false'
            if isinstance(v, (int, float)):
                return str(v)
            if isinstance(v, set):
                v = list(v)
            if isinstance(v, (list, tuple, dict)):
                return json.dumps(v)
        except Exception:
            return None
        return None

    @staticmethod
    def value_to_node_type(v: (int, float, bool, str, list, set, tuple, dict, type(None))) -> (str, type(None)):
        """
        根据给定的节点的合法值，推断节点类型
        :param v: 需要被推断类型值
        :return:
            成功 节点类型
            失败 None
        """
        type_map = {str: 'str',
                    float: 'float',
                    int: 'int',
                    bool: 'bool',
                    list: 'list',
                    tuple: 'list',
                    set: 'list',
                    dict: 'dict',
                    type(None): 'str'}
        # noinspection PyBroadException
        try:
            return type_map[type(v)]
        except Exception:
            return None
    # endregion

    # region 类属性
    @property
    def key(self):
        return self.__key

    @property
    def full_key(self):
        return self.to_std_node_path(*self.__full_key)

    @property
    def idx(self):
        return self.generate_node_idx(*self.__full_key)

    @property
    def value(self):
        return self.__value

    @property
    def type(self):
        return self.__type

    @property
    def level(self):
        return self.__level

    @property
    def father(self):
        return self.to_std_node_path(*self.__father)

    @property
    def father_idx(self):
        return self.generate_node_idx(*self.__father)

    @property
    def storage(self):
        """
        返回该node在数据库中实际存储的值：
        对于RealCfg来说，不管node的值是什么，最终都是转成 字符串 存在数据库中的
        并且该字符串要 "符合json规范"
        所以，Node的各种值需要转换成对应的Json表示形式
        注意：
            此属性返回的数据，是为了实现 "真实值" <-> "Json格式的存储值" 之间的转换
            并非/并非/并非 "真实值" <-> "sql语句中表示形式" 之间的转换
        :return:
        """
        value_for_storage = self.value_to_storage(self.value)
        if value_for_storage is None:
            raise ValueError('found an exceptional RealCfgValue value <{}, {}>'.format(self.value, type(self.value)))
        return value_for_storage
    # endregion
