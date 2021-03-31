# -*- coding: UTF-8 -*-

from typing import Any, Callable
from operator import lt as optor_lt, gt as optor_gt


def float_pro(value: Any) -> float:
    """
    增强的float类型转换函数，可以处理数值字符串中含有逗号的情况
    :param value: 需要转换成float的值
    :return: 转换后的float
    """
    if isinstance(value, str):
        value = value.replace(',', '')
        value = value.replace('，', '')
    # noinspection PyBroadException
    try:
        return float(value)
    except Exception:
        return 0.0


def str_pro(value: Any) -> str:
    """
    增强的str类型转换函数，可以强转任何value到str
    :param value: 需要转换成str的值
    :return: 转换后的str
    """
    return '{}'.format(value)


def int_pro(value: Any) -> int:
    """
    增强的int类型转换函数，可以处理数值字符串中含有逗号的情况
    :param value: 需要转换成float的值
    :return: 转换后的float
    """
    if isinstance(value, str):
        value = value.replace(',', '')
        value = value.replace('，', '')
    # noinspection PyBroadException
    try:
        return int(value)
    except Exception:
        return 0


def is_number(desc: str) -> bool:
    """
    判断指定的字符串是否是一个数字（整数、浮点数）
    :param desc: 待判断的字符串
    :return:
        True  是
        False 不是
    """
    if '.' in desc:
        secs = desc.split('.')
        if len(secs) > 2:
            return False
        if not secs[0].isdecimal():
            return False
        if len(secs[1]) > 0 and not secs[1].isdecimal():
            return False
        return True
    return desc.isdecimal()


class RealLLNode(object):
    """
    双向链表RealLL的结点
    """
    def __init__(self, value: Any, left_node: 'RealLLNode' = None, right_node: 'RealLLNode' = None):
        super(RealLLNode, self).__init__()
        self.value = value
        self.left = left_node
        self.right = right_node
        self.me = self  # 普通节点的self.me指向自身，用作RealLL两个特殊out端点时，self.me会被置为None

    def __str__(self) -> str:
        return str(self)

    def next(self, reverse: bool = False):
        if reverse:
            return self.left.me
        return self.right.me

    def hive_off(self):
        """
        节点将自身从链表中摘除
        :return: 节点自身
        """
        left = self.left
        right = self.right
        if left is not None:
            left.right = right
        if right is not None:
            right.left = left
        self.left = None
        self.right = None
        return self

    def insert_at_left(self, another_node: 'RealLLNode'):
        """
        将指定的链表节点插到自己的左侧
        函数强制认为插到左侧的新节点是一个“hive off”状态的离群节点，即此节点的left、right信息将被无视
        :param another_node: 待插入的节点
        :return:
        """
        another_node.left = self.left
        another_node.right = self
        self.left.right = another_node
        self.left = another_node
        return

    def insert_at_right(self, another_node: 'RealLLNode'):
        """
        将指定的链表节点插到自己的右侧
        函数强制认为插到右侧的新节点是一个“hive off”状态的离群节点，即此节点的left、right信息将被无视
        :param another_node: 待插入的节点
        :return:
        """
        another_node.left = self
        another_node.right = self.right
        self.right.left = another_node
        self.right = another_node
        return


class RealLLIter(object):
    """
    双向链表RealLL的迭代器
    """
    def __init__(self, node: (RealLLNode, type(None))):
        self.curr_node = node if isinstance(node, RealLLNode) and node.me is not None else None

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_node is None:
            raise StopIteration
        value_out = self.curr_node.value
        self.curr_node = self.curr_node.next()
        return value_out


class RealLL(object):
    """
    双向链表
        > 可在两侧push和pop
        > 可迭代
        > 可随机访问（切片），效率低！
    """

    # region 重写
    """
    """
    def __init__(self):
        super(RealLL, self).__init__()
        # 初始链表为空
        self.__leftout = RealLLNode(None, None, None)  # 最左元素（内部使用，永远不变，不用于存值）
        self.__rightout = RealLLNode(None, None, None)  # 最右元素（内部使用，永远不变，不用于存值）
        self.__leftout.right = self.__rightout
        self.__leftout.me = None  # 将node的me属性置为none，后续通过node.me获取node时，就可以安全获取数据了
        self.__rightout.left = self.__leftout
        self.__rightout.me = None  # 将node的me属性置为none，后续通过node.me获取node时，就可以安全获取数据了
        self.__len = 0  # 链表长度
        self.__sort_engine = {'merge': self.__merge_sort,
                              'quick': self.__quick_sort,
                              'heap': self.__heap_sort,
                              'tim': self.__tim_sort,
                              'default': self.__merge_sort}
        return

    def __iter__(self):
        return RealLLIter(self.__leftout.right)

    def __getitem__(self, idx):
        if isinstance(idx, int):
            if idx > (self.__len - 1):
                raise IndexError('IndexError: {} is out of index (total {})'.format(idx, self.__len))
            for value in self:
                if 0 == idx:
                    return value
                idx -= 1
        if isinstance(idx, slice):
            start = self.__len + idx.start if idx.start < 0 else idx.start
            stop = self.__len + idx.stop if idx.stop < 0 else idx.stop
            if stop < 0 or start < 0 or stop <= start:
                return []
            values = []
            cur = -1
            for value in self:
                cur += 1
                if cur < start:
                    continue
                if cur >= stop:
                    break
                values.append(value)
            return values
        raise TypeError('TypeError: index access for RealLL need a integer or slice, but {} instead'.format(type(idx)))

    def __len__(self):
        return self.__len

    def __del__(self):
        # 释放两个固定左右端点，解除它们之间的互引用
        self.__leftout.left = None
        self.__leftout.right = None
        self.__rightout.left = None
        self.__rightout.right = None
    # endregion

    # region 属性
    """
    """
    @property
    def leftest(self):
        return self.__leftout.right.me

    @property
    def rightest(self):
        return self.__rightout.left.me
    # endregion

    # region 静态方法
    """
    """
    @staticmethod
    def swap_nodes(node_a: RealLLNode, node_b: RealLLNode):
        """
        交换两个节点在链表中的位置
        这里不做“两个节点是否在一个链表中的判断”，效率太低了，也就是说不管在不在一个链表之内，都会交换
        :param node_a: 待交换位置的节点
        :param node_b: 待交换位置的节点
        :return:
        """
        node_a.value, node_b.value = node_b.value, node_a.value
        return

    @staticmethod
    def __sorted_items_merge(left_left: RealLLNode,
                             right_left: RealLLNode,
                             left_len: int,
                             right_len: int,
                             cmptor: Callable):
        """
        将链表中相邻的两节有序节点片段合并成一个新的有序片段，并仍然拼接在源片段在链表中的原位置
        需要两个片段都遵从同样的顺序，并且最后输出的合并结果也将是同样的顺序
        仅用于归并排序
        :param left_left: 源片段a的最左端节点
        :param right_left: 源片段b的最左端节点
        :param left_len: 源片段a的长度
        :param right_len: 源片段b的长度
        :param cmptor: 比较运算符（目标顺序左小右大时应为lt，左大右小时应为gt）
        :return:
        """
        idx_left = 0
        idx_right = 0
        left_item = left_left
        right_item = right_left
        while True:
            if idx_left == left_len or idx_right == right_len:
                # 其中一个片段已经全都找到了位置
                # 结束合并
                break
            if cmptor(right_item.value, left_item.value):
                # 如果右侧片段当前位置item的值"x"于左侧片段当前item的值（与目标顺序逆序）
                # 将右侧片段当前item剥离，然后插入到左侧片段比它"x"的那个item左侧
                # 右侧当前item向右移一格
                curr_right = right_item
                right_item = right_item.right
                idx_right += 1
                left_item.insert_at_left(curr_right.hive_off())
            else:
                # 如果右侧片段当前位置item的值不"x"于左侧片段当前item的值时（与目标顺序同序）
                # 左侧片段的当前item向右移一格
                idx_left += 1
                left_item = left_item.right
        return

    @staticmethod
    def __merge_sort(left_node: RealLLNode, ll_len: int, cmptor: Callable):
        """
        对指定开头和长度的链表片段做归并排序
        这里没有使用递归，而是直接展开成了循环
        :param left_node: 待排序的链表的左端点
        :param ll_len: 待排序的链表长度
        :param cmptor: 比较运算符
        :return:
        # TODO：和list自带的sort（timsort）相比，速度查了100倍，MLGBD ……
        """
        if ll_len <= 0:
            return
        already_sorted_sec = RealLL()
        already_sorted_sec.rpush([0, None, None])  # 在等待merge的队列开头放一个初始sec（空，长度标记为0）
        cmp_start = left_node  # 从待排序的列表的最左元素开始两两比较
        for i in range(0, ll_len//2*2, 2):
            left_one = cmp_start  # 待两两比较的 左元素
            right_one = left_one.next()  # 待两两比较的 右元素
            next_start = right_one.next()  # 下一组两两比较的元素的 左元素（要在这里准备好，不能在后面通过right_one获取）
            if cmptor(right_one.value, left_one.value):
                # 如果右元素"x"于左元素，交换二者的位置
                RealLL.swap_nodes(right_one, left_one)
            new_sec = [2, left_one, right_one]  # 用当前比较结果生成一个有序sec
            while len(already_sorted_sec) > 0:
                # 尝试与已经生成的有序sec合并，直到遇到长度断层
                last_sec = already_sorted_sec.rightest.value
                if last_sec[0] > new_sec[0]:
                    # 遇到长度断层，结束合并
                    break
                already_sorted_sec.rpop()  # 合并之前，将待合并的有序sec从sec序列中取出
                left_out = new_sec[1].left if last_sec[1] is None else last_sec[1].left  # 这两个sec的左外界
                right_out = new_sec[2].right  # 这两个sec的右外界
                RealLL.__sorted_items_merge(last_sec[1], new_sec[1], last_sec[0], new_sec[0], cmptor)  # 合并
                new_sec = [last_sec[0]+new_sec[0], left_out.right, right_out.left]  # 利用左右外界获取合并后sec的左右元素
            already_sorted_sec.rpush(new_sec)  # 合并后的有序sec放到sec序列末尾
            cmp_start = next_start  # 准备下一个比较起始点
        if 0 == ll_len % 2:
            # 如果结尾没有单独的元素，所有需要排序的元素都在sec序列里面了
            # 先取出最后一个
            new_sec = already_sorted_sec.rpop()
        else:
            # 如果结尾还剩一个元素没有比较、排序
            # 单独作为一个sec放到sec序列
            new_sec = [1, cmp_start, cmp_start]
        while len(already_sorted_sec) > 0:
            # 所有的元素都已经放入或大或小的有序sec，合并这些sec到一起，完成排序
            last_sec = already_sorted_sec.rpop()
            if last_sec[1] is None:
                # 没有待合并的sec，不需要合并（整个链表只有一个元素）
                break
            if last_sec[1] is None:
                left_out = new_sec[1].left  # 这两个sec的左外界
            else:
                left_out = last_sec[1].left  # 这两个sec的左外界
            right_out = last_sec[2].right if new_sec is None else new_sec[2].right  # 这两个sec的右外界
            RealLL.__sorted_items_merge(last_sec[1], new_sec[1], last_sec[0], new_sec[0], cmptor)  # 合并
            new_sec = [last_sec[0] + new_sec[0], left_out.right, right_out.left]  # 利用左右外界获取合并后sec的左右元素
        return

    @staticmethod
    def __quick_sort(left_node: RealLLNode, ll_len: int, cmptor: Callable):
        """
        对指定开头和长度的链表片段做快速排序
        :param left_node: 待排序的链表的左端点
        :param ll_len: 待排序的链表长度
        :param cmptor: 比较运算符
        :return:
        """
        if not ll_len > 0:
            return
        # TODO：尚未实现
        return

    @staticmethod
    def __heap_sort(left_node: RealLLNode, ll_len: int, cmptor: Callable):
        """
        对指定开头和长度的链表片段做堆排序
        :param left_node: 待排序的链表的左端点
        :param ll_len: 待排序的链表长度
        :param cmptor: 比较运算符
        :return:
        """
        if not ll_len > 0:
            return
        # TODO：尚未实现
        return

    @staticmethod
    def __tim_sort(left_node: RealLLNode, ll_len: int, cmptor: Callable):
        """
        对指定开头和长度的链表片段做tim排序
        :param left_node: 待排序的链表的左端点
        :param ll_len: 待排序的链表长度
        :param cmptor: 比较运算符
        :return:
        """
        if not ll_len > 0:
            return
        # TODO：尚未实现
        return

    # endregion

    # region 内部函数
    """
    """
    # endregion

    # region 实例方法
    """
    """
    def lpush(self, value: Any):
        new_node = RealLLNode(value)  # 创建新node
        self.__leftout.insert_at_right(new_node)  # 链接到固定最左元素的右侧
        self.__len += 1
        return

    def lpop(self):
        if 0 == self.__len:
            raise ValueError('PopError: empty real link list')
        self.__len -= 1
        return self.__leftout.right.hive_off().value

    def rpush(self, value: Any):
        new_node = RealLLNode(value)  # 创建新node
        self.__rightout.insert_at_left(new_node)
        self.__len += 1
        return

    def rpop(self):
        if 0 == self.__len:
            raise ValueError('PopError: real link list is empty')
        self.__len -= 1
        return self.__rightout.left.hive_off().value

    def append(self, value: Any):
        self.rpush(value)
        return

    def sort(self, desc: bool = False, engine: str = 'merge'):
        """
        链表元素排序，要求列表内元素满足任何两个元素可比较大小
        :param desc: 是否降序
        :param engine: 排序引擎
                           > 'merge' 归并排序
                           > 'quick' 快速排序
                           > 'heap' 堆排序
        :return:
        """
        engine = engine if engine in self.__sort_engine else 'default'
        cmptor = optor_gt if desc else optor_lt
        try:
            self.__sort_engine[engine](self.__leftout.right, self.__len, cmptor)
        except KeyError:
            ...
        except Exception as err:
            raise err
        return
    # endregion


class NoOneIsMe(object):
    def __init__(self):
        super(NoOneIsMe, self).__init__()
        self.Label = 'No one is me'
