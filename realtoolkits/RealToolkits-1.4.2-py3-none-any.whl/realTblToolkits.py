# -*- coding: UTF-8 -*-

import os
import re
import csv
from ctypes import CDLL
import chardet
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ETr
from xml.etree.ElementTree import Element as Et
from .ExcelMeta import get_xlsx_meta_fast, get_xls_meta
from .type_kits import NoOneIsMe, str_pro, float_pro, int_pro


# xml格式excel表格操纵类
class XMLExcel(object):
    """
    """

    # region 重写
    """
    """
    def __init__(self, fn: str, snap_size: int = 200):
        super(XMLExcel, self).__init__()
        self.LastErr = None
        self.__is_valid = False
        # 检查快照行数参数
        if not isinstance(snap_size, int) or snap_size < 0:
            self.LastErr = '为文件 {} 指定了一个非法的 snapsize 参数: {}'.format(fn, snap_size)
            return
        # 检查fn是否是一个xml文件
        if not isinstance(fn, str) or not os.path.isfile(fn):
            self.LastErr = '{} {} 不是一个合法文件名，或文件不存在'.format(fn, type(fn))
            return
        if not self.may_be_xml(fn):
            self.LastErr = '{} 不是一个xml文件'.format(fn)
            return
        # 读取根节点
        try:
            tree = ETr.parse(fn)  # 打开xml文档
            root = tree.getroot()  # 获得root节点
        except Exception as err:
            self.LastErr = '打开文件失败：{}'.format(err)
            return
        # 检查文件是否有xml格式excel表格必须的节点
        if not self.__is_valid_xml_excel(root):
            self.LastErr = '文件不是有效的xml格式的excel表格'
            return
        # 提取文件元数据
        sheets_info = {'sheet_names_*': []}
        for level1_child in root:
            # 找出所有工作表
            tmp_tag = level1_child.tag.strip()
            tmp_pure_tag = tmp_tag.split('}')[-1].lower()
            if tmp_pure_tag != 'worksheet':
                continue
            sheet_name = self.__get_sheet_name_from_arrtib(level1_child.attrib)  # 提取sheet名称
            if sheet_name is None:
                self.LastErr = '无法从节点属性 {} 中找到节点 {} 的名称'.format(level1_child.attrib, level1_child.tag)
                continue
            sheets_info['sheet_names_*'].append(sheet_name)  # 记录找到的sheet信息
            sheets_info[sheet_name] = {'element': level1_child, 'tag': tmp_tag}
        meta = {'sheet_names_*': []}
        meta_ext = dict()
        for sheet_name in sheets_info['sheet_names_*']:
            # 提取每个工作表的元数据信息
            sheet_node = sheets_info[sheet_name]['element']
            sheet_tag = sheets_info[sheet_name]['tag']
            sheet_meta_ext = {'sheet_urn': sheet_tag[:-8], 'sheet_pure_tag': sheet_tag[-8:]}
            sheet_meta = self.__get_xml_sheet_meta(sheet_node, sheet_meta_ext, snap_size)
            if sheet_meta is not None:
                # 记录成功提取到元数据的工作表信息
                # 找不到元数据的工作表，就扔掉了
                meta['sheet_names_*'].append(sheet_name)
                meta[sheet_name] = sheet_meta
                meta_ext[sheet_name] = sheet_meta_ext
        if 0 == len(meta):
            # 一个有效的worksheet都没有
            return
        # 记录表格数据，改变类实体状态为可用
        self.__fn = fn
        self.__meta = meta
        self.__meta_ext = meta_ext
        self.__workbook_urn = root.tag.strip()[:-8]
        self.__workbook_pure_tag = root.tag.strip()[-8:]
        self.__is_valid = True
        return

    def __str__(self):
        curr_meta = self.meta
        if curr_meta is None:
            return 'Valid: {} <no meta data found>'.format(self.__is_valid)
        desc = str(curr_meta['sheet_names_*'])+'\n'
        for sheet_name in curr_meta['sheet_names_*']:
            sheet_meta = curr_meta[sheet_name]
            desc += '    {}: {}* {} （行 * 列）'.format(sheet_name, sheet_meta['rows'], sheet_meta['cols'])
            desc += '\n        {}'.format(sheet_meta['snap'][0].tolist())
            desc += '\n        {}'.format(sheet_meta['snap'][1].tolist())
        return desc
    # endregion

    # region 类静态方法
    """
    """
    # 是否是一个合法的xml格式excel文件
    @staticmethod
    def __is_valid_xml_excel(root_node: Et) -> bool:
        if not isinstance(root_node, Et):
            return False
        if 'workbook' != root_node.tag[-8:].lower():
            return False
        must_have = {'documentproperties', 'excelworkbook', 'styles', 'worksheet'}  # 合法xml格式excel文件的必须节点
        test_times = 0
        for level1_child in root_node:
            tmp_tag = level1_child.tag.split('}')[-1].strip().lower()
            # 检查每一个子节点是否是合法xml格式excel文件的必须节点
            if tmp_tag in must_have:
                must_have.remove(tmp_tag)
                if 0 == len(must_have):
                    # 已经找齐，直接返回是合法的xml格式excel文件
                    return True
            test_times += 1
            if test_times >= 100:
                # 检查了根节点下100个第一层子节点，还是没找齐必须节点
                # 认为不是合法xml格式excel文件
                return False
        if len(must_have) > 0:
            # 遍历了所有第一层子节点，也没有找齐
            # 不是合法xml格式excel文件
            return False
        return True

    # 是否可能是一个xml文件
    @staticmethod
    def may_be_xml(fn: str) -> bool:
        # noinspection PyBroadException
        try:
            with open(fn, mode='rb') as f:
                head_bytes = f.read(5)
                first_line = head_bytes.decode('utf8')
                first_line = first_line.strip().lower()
                if len(first_line) < 5 or '<?xml' != first_line[:5]:
                    return False
        except Exception:
            return False
        return True

    # 从worksheet的attrib中提取sheet名称
    @staticmethod
    def __get_sheet_name_from_arrtib(attribs: dict) -> (str, type(None)):
        # noinspection PyBroadException
        try:
            for attr_key in attribs:
                if 'name' == attr_key.split('}')[-1].strip().lower():
                    return attribs[attr_key]
        except Exception:
            return None
        return None

    # 将一个二维list的每一行对齐到一个宽度
    @staticmethod
    def __align_two_dimensional_list(two_dimensional_list: list, width: int) -> bool:
        # noinspection PyBroadException
        try:
            row_num = len(two_dimensional_list)
            for i in range(row_num):
                # 统一row（行）数据到同一个宽度
                each_row_len = len(two_dimensional_list[i])
                if each_row_len >= width:
                    # 宽了剪
                    two_dimensional_list[i] = two_dimensional_list[i][:width]
                elif each_row_len < width:
                    # 窄了补
                    two_dimensional_list[i].extend([None] * (width - each_row_len))
        except Exception:
            return False
        return True

    # 从xml格式excel文件的一个row中读取所有cell数据
    @staticmethod
    def __get_row_data(row_node: Et) -> list:
        rlst = []
        for may_be_cell in row_node:
            # 遍历row中的每个cell
            if '}cell' != may_be_cell.tag[-5:].lower():
                continue
            # 提取每个cell的DATA节点的值
            rlst.append(may_be_cell[0].text if len(may_be_cell) > 0 else None)
        return rlst

    # 生成一个工作表的快照
    @staticmethod
    def __get_xml_sheet_meta(sheet_node: Et, sheet_info: dict, snap_size: int) -> (dict, type(None)):
        # noinspection PyBroadException
        try:
            # 在sheet中找第一个table节点
            # 注意：这里有一个默认行为，认为一个sheet里只有一个table（没查到资料，这一点并不保证）
            table_node = None
            for may_be_table in sheet_node:
                table_tag = may_be_table.tag.strip()
                if 'table' != table_tag[-5:].lower():
                    continue
                table_node = may_be_table
                sheet_info['table'] = may_be_table
                sheet_info['table_urn'] = table_tag[:-5]  # 这里修改了传入的参数，以记录table的urn
                sheet_info['table_pure_tag'] = table_tag[-5:]  # 这里修改了传入的参数，以记录table的urn
                break
            if table_node is None:
                # 找不到table节点
                return None
            # 找到table节点，提取table数据
            result = {'rows': None, 'cols': None, 'snap': None}
            col_count_key = sheet_info['table_urn'] + 'ExpandedColumnCount'
            row_count_key = sheet_info['table_urn'] + 'ExpandedRowCount'
            result['rows'] = int(table_node.attrib[row_count_key])  # 表格行数
            result['cols'] = int(table_node.attrib[col_count_key])  # 表格列数
            snap_list = []
            for may_be_row in table_node:
                # 遍历table节点中的每个row（行），提取row（行）数据
                row_tag = may_be_row.tag.strip()
                if '}row' != row_tag[-4:].lower():
                    continue
                row_data = XMLExcel.__get_row_data(may_be_row)
                # 统一row（行）数据到同一个宽度
                each_row_len = len(row_data)
                if each_row_len >= result['cols']:
                    # 宽了剪
                    row_data = row_data[:result['cols']]
                elif each_row_len < result['cols']:
                    # 窄了补
                    row_data.extend([None] * (result['cols'] - each_row_len))
                # 存储这一行的数据
                snap_list.append(row_data)
                snap_size -= 1
                if 0 == snap_size:
                    # 如果获得的row已经达到快照要求的行数，就不再往下读了
                    break
            # 构建快照ndArray，放到sheet meta结构中
            real_snap_row_size = len(snap_list)
            if real_snap_row_size < snap_size and real_snap_row_size < result['rows']:
                result['rows'] = real_snap_row_size
            if real_snap_row_size > 0:
                result['snap'] = np.array(snap_list)
        except Exception:
            return None
        return result

    # 从list/tuple中挑选指定下标的数据，形成一个新的list
    @staticmethod
    def __filter_list_by_idx(data: (list, tuple), idxs: (list, tuple)) -> (list, type(None)):
        # noinspection PyBroadException
        try:
            new_data = []
            for idx in idxs:
                new_data.append(data[idx])
        except Exception:
            return None
        return new_data

    # 直接读取一个xml格式excel文件到df
    @staticmethod
    def directly_read_sheet(fn: str, **kwargs):
        """
        不通过XMLExcel实例直接读取一个xml到df（中间会生生一个临时的XMLExcel实例）
        :param fn: 文件名
        :param kwargs: 读取参数
        :return:
            成功  DF
            失败  None
        """
        xml_excel = XMLExcel(fn)
        if xml_excel is None:
            return None
        sheet_name = None
        if 'sheet_name' in kwargs:
            sheet_name = kwargs['sheet_name']
            del kwargs['sheet_name']
        return xml_excel.read_sheet(sheet_name, **kwargs)
    # endregion

    # region 属性
    """
    """
    @property
    def fn(self) -> (str, type(None)):
        return self.__fn if self.__is_valid else None

    @property
    def meta(self) -> (dict, type(None)):
        return self.__meta if self.__is_valid else None

    # endregion

    # region 实体成员方法
    """
    """
    # 获取指定的sheet表在xml文件中的path
    def table_path(self, sheet_name: str) -> (str, type(None)):
        if not self.__is_valid:
            return None
        try:
            sheet_full_tag = self.__meta_ext[sheet_name]['sheet_urn']+self.__meta_ext[sheet_name]['sheet_pure_tag']
            table_full_tag = self.__meta_ext[sheet_name]['table_urn']+self.__meta_ext[sheet_name]['table_pure_tag']
            table_path = '{}/{}/'.format(sheet_full_tag, table_full_tag)
        except KeyError:
            return None
        return table_path

    # 将指定的sheet表读入DF
    def read_sheet(self, sheet_name: str = None, **kwargs):
        """
        读取
        :param sheet_name: 要读取的sheet页的名称，不提供则读取sheet页列表中的第一个
        :param kwargs: 读取参数，兼容pandas.read_excel的读取参数
                       当前已经支持的有 usecols, names, converters, header，其它的将被忽略
        :return:
            成功  DF
            失败  None
        """
        # 函数只能在自身状态有效的情况下使用
        if not self.__is_valid:
            return None
        # 参数检查/规范化
        if sheet_name is None:
            sheet_name = self.meta['sheet_names_*'][0]
        if sheet_name not in self.meta:
            return None
        # 提取读取参数
        sheet_meta = self.meta[sheet_name]
        col_count = sheet_meta['cols']
        try:
            header = kwargs['header']
            header = 0 if not isinstance(header, int) or header < 0 else header
        except KeyError:
            header = 0
        try:
            usecols = kwargs['usecols']
            usecols = [i for i in range(col_count)] if not isinstance(usecols, (list, tuple)) else usecols
            for value in usecols:
                if not isinstance(value, int) or value < 0 or value >= col_count:
                    self.LastErr = 'read_sheet在usecols中发现非法数据：{}'.format(usecols)
                    return None
        except KeyError:
            usecols = [i for i in range(col_count)]
        try:
            names = kwargs['names']
            if not isinstance(names, (list, tuple)) or len(names) != len(usecols):
                self.LastErr = 'read_sheet发现names非法：{} （usecols = {}）'.format(names, usecols)
                return None
            for i in range(len(names)):
                if not isinstance(names[i], str):
                    names[i] = str_pro(names[i])
        except KeyError:
            names = None
        try:
            converters = kwargs['converters']
            if not isinstance(converters, dict):
                self.LastErr = 'read_sheet发现converters容器非法：{}'.format(converters)
                return None
            del_converters = []
            for idx in converters:
                if type(idx) is not int:
                    self.LastErr = 'read_sheet发现converters列idx不是int：{} {} in {}'.format(idx, type(idx), converters)
                    return None
                if idx < 0 or idx > len(usecols)-1:
                    self.LastErr = 'read_sheet发现converters列idx值不在[0,{}]范围'.format(len(usecols)-1)
                    return None
                if converters[idx] is str or converters[idx] is str_pro:
                    del_converters.append(idx)
            for idx in del_converters:
                # 从xml读取的数据全是str，不用特意转换
                del converters[idx]
        except KeyError:
            converters = None
        # 获取table节点
        first_table = self.__meta_ext[sheet_name]['table']
        """
        try:
            # 重新打开xml文档
            tree = ETr.parse(self.fn)
            # 获取root节点
            root = tree.getroot()
            # 生成table节点的path
            table_path = self.table_path(sheet_name)
            if table_path is None:
                self.LastErr = 'read_sheets生成 {} 的table_path失败：{}'.format(sheet_name, self.__meta_ext[sheet_name])
                return None
            first_table = root.find(table_path)
            if first_table is None:
                self.LastErr = 'read_sheet无法找到path为 {} 的table节点'.format(table_path)
                return None
        except Exception as err:
            self.LastErr = 'read_sheet获取table节点失败：{}'.format(err)
            return None
        """
        # 从table中获取所有row节点
        try:
            snap_list = []
            for may_be_row in first_table:
                # 遍历table节点中的每个row（行），提取row（行）数据
                row_pure_tag = may_be_row.tag.strip()[-4:].lower()
                if '}row' != row_pure_tag:
                    continue
                row_data = XMLExcel.__get_row_data(may_be_row)
                snap_list.append(row_data)
        except Exception as err:
            self.LastErr = 'read_sheet获取所有row失败： {}'.format(err)
            return None
        # 统一row（行）数据到同一个宽度
        if not self.__align_two_dimensional_list(snap_list, self.meta[sheet_name]['cols']):
            self.LastErr = 'read_sheet统一读取的row宽度到 {} 失败'.format(self.meta[sheet_name]['cols'])
            return None
        # 将读取的所有row，根据读取参数转换成最终的df
        try:
            # 根据header对row数据横向切片，生成初始DF
            rows_needed = snap_list[header+1:]
            tmp_df = pd.DataFrame(data=rows_needed, columns=snap_list[header])
            # 根据usecols信息对初始DF纵向切片，只保留需要的列
            title_neede = self.__filter_list_by_idx(snap_list[header], usecols)
            cols_needed = tmp_df[title_neede].copy()
            # 根据converter信息，修改数据列的类型
            if converters is not None:
                for cvt_idx in converters:
                    col_name = title_neede[cvt_idx]
                    cols_needed[col_name] = cols_needed[col_name].map(lambda x: converters[cvt_idx](x))
            # 修改df列名
            if names is not None:
                cols_needed.columns = names
        except Exception as err:
            self.LastErr = 'read_sheet转换row到df失败： {}'.format(err)
            return None
        return cols_needed
    # endregion


class TableMeta(object):
    """
    表格文件元数据类
    根据文件名，自动生成表格文件的元数据
    提供在快照覆盖范围内的一些数据操作
    """

    # region 重写
    """
    """
    def __new__(cls, fn: str, dll: (CDLL, type(None)) = None):
        # 参数检查
        if not isinstance(fn, str):
            return None
        fn = fn.strip()
        if '' == fn:
            return None
        if not isinstance(dll, (CDLL, type(None))):
            dll = None
        # 文件合法性检查
        ext_name = fn.split('.')[-1].lower()
        if ext_name not in ('xlsx', 'xls', 'csv', 'txt', 'xml'):
            # 不是这五种文件，不支持
            return None
        # 检查文件是否存在
        if not os.path.isabs(fn):
            fn = os.path.join(os.path.abspath('.'), fn)
        if not os.path.isfile(fn):
            # 文件不存在
            return None
        # 记录文件信息
        be_self = super(TableMeta, cls).__new__(cls)
        if be_self is None:
            return None
        be_self.__fn = fn
        be_self.__ext_name = ext_name
        be_self.__is_csv = True if ext_name in ('csv', 'txt') else False
        be_self.__is_xml = True if ext_name == 'xml' else XMLExcel.may_be_xml(fn)
        # 读取表格快照信息
        be_self.__snap_size = 200
        if be_self.__is_csv:
            # CSV文件
            tmp_snap = TableMeta.snapshot_csv(fn, be_self.__snap_size)
        elif be_self.__is_xml:
            # xml文件
            xml_excel = XMLExcel(fn, be_self.__snap_size)
            tmp_snap = xml_excel.meta
        elif 'xlsx' == ext_name:
            # xlsx 文件
            tmp_snap = get_xlsx_meta_fast(fn, be_self.__snap_size, dll)
        else:
            # xls 文件
            tmp_snap = get_xls_meta(fn, be_self.__snap_size)
        if tmp_snap is None:
            return None
        # 记录表格快照信息
        be_self.__snap = tmp_snap
        return be_self

    def __init__(self, fn: str, dll: (CDLL, type(None)) = None):
        super(TableMeta, self).__init__()
        self.__orign_fn = fn.strip()
        self.__dll_name = '{}'.format(dll)
        return
    # endregion

    # region 静态工具函数
    """
    """
    # 检测文本文件的编码
    @staticmethod
    def check_txt_encoding(fn: str) -> (list, type(None)):
        """
        检查文本文件编码
        :param fn: 文件名（含路径）
        :return:
            成功  ['编码字符串', ...]
            失败  None
        """
        # 字节方式读取文件开头部分字节
        # （判断编码不需要太长）
        # noinspection PyBroadException
        try:
            read_len = 300  # 文本文件采样长度
            with open(file=fn, mode='rb') as xf:
                data_buff = xf.read(read_len)
        except Exception:
            return None
        # 判断文件编码
        tmp_rlst = chardet.detect(data_buff)
        rlst_confidence = tmp_rlst['confidence']
        rlst_encoding = tmp_rlst['encoding']
        if 'GB2312' == rlst_encoding:
            # GBK是GB2312的超集，如果判定为GB2312，统一用GBK代替
            rlst_encoding = 'GBK'
        # 生成所有需要尝试的编码集合
        all_encodings = [] if rlst_confidence < 0.7 else [rlst_encoding]
        if 'utf-8' not in all_encodings:
            # 补充最常用的UTF8
            all_encodings.append('utf-8')
        if 'GBK' not in all_encodings:
            # 补充最常用的GBK
            all_encodings.append('GBK')
        return all_encodings

    # 监测csv文件的分隔符
    @staticmethod
    def check_csv_sep(fn: str, encodings: list):
        """
        监测csv文件的分隔符
        分隔符限制为ASC码小于128、非字母、非数字、非空格、非双引号的单个可见字符（含\t）
        :param fn: csv文件名
        :param encodings: csv文件编码
        :return:
            成功  分隔符
            失败  None
        """
        # 读取样本
        sample_lines = 40  # 样本行数
        sample = []
        for each_encoding in encodings:
            # noinspection PyBroadException
            try:
                with open(fn, mode='r', encoding=each_encoding) as sample_file:
                    while len(sample) < sample_lines:
                        line = sample_file.readline()
                        if '' == line:
                            # 文件结束，不足 sample_lines 行
                            break
                        line = line.replace('""', '')  # 存储样本行之前要做一定的处理： 剔除 双双引号
                        line = re.sub('".+?"', '', line)  # 存储样本行之前要做一定的处理： 剔除""内部的内容，免得影响列数统计
                        sample.append(line)
                # 使用当前编码读取成功
                break
            except UnicodeDecodeError:
                # 编码不正确，换下一个编码尝试
                sample = []
                continue
            except Exception:
                # 非编码错误的异常，无法判断分隔符
                return None
        if 0 == len(sample):
            # 无法解析文件编码 or 空文件
            return None
        # 根据样本分析最可能的分隔符
        # 样本行掐头去尾，尽可能保留中间10行
        sample_lines = len(sample)
        if 0 == sample_lines:
            # 空文件
            return None
        elif sample_lines > 10:
            start = int((sample_lines - 10) / 2) + 1
            sample = sample[start:start+10]
        # 提取每一行可能做分隔符的字符集
        whole_set = {',', '!', '#', '$', '%', '&', "'", '(', ')', '*', '+',
                     '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '\t',
                     '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~'}
        for line in sample:
            whole_set = whole_set & set(line)
            if 0 == len(whole_set):
                # 如果各行之间不存在共同的分隔符
                # 则保留一个英文逗号，这样的话只有一列的场景能够正常被处理
                whole_set.add(',')
                break
        # 检测剩下的各个可能的字符是否能将每行分割成相同的列数
        possible_sep_info = dict()
        for possible_sep in whole_set:
            possible_sep_info[possible_sep] = set()
            for line in sample:
                possible_sep_info[possible_sep].add(line.count(possible_sep))
        # 如果有多个可以分割出相同列数的分隔符，选取列数最多的那个
        sep_nums = 1  # 分隔符在一行中出现的次数（和列数等价）
        sep = None  # 最终的分隔符
        for possible_sep in possible_sep_info:
            if len(possible_sep_info[possible_sep]) > 1:
                # 如果这个分隔符分割出的列数不一样，则抛弃
                continue
            # 如果这个分隔符分割出的列数最多
            # 则暂存这个分隔符作为最后的结果
            if max(possible_sep_info[possible_sep]) > sep_nums:
                sep_nums = max(possible_sep_info[possible_sep])
                sep = possible_sep
        if sep is not None:
            return sep
        if sep is None:
            # 实践发现，下面两段臆测的逻辑效果并不好
            # 更可能导致这里仍然找不到sep的情况是数据列内部含有回车，一行被错误的折行读取
            # 所以这里改为，如果找不到可以分割出相同列数的分隔符，就强行用','
            # 下面两段逻辑永远不会再去执行了
            return ','
        # 如果所有的分隔符都不能分割出相同的列
        # 选取分割出的列数量种类最少的分隔符
        del_seps = []
        keep_seps = []
        min_line_count_type = 10000000
        for possible_sep in possible_sep_info:
            if len(possible_sep_info[possible_sep]) > min_line_count_type:
                del_seps.append(possible_sep)
            elif len(possible_sep_info[possible_sep]) == min_line_count_type:
                keep_seps.append(possible_sep)
            else:
                del_seps.extend(keep_seps)
                keep_seps = [possible_sep]
                min_line_count_type = len(possible_sep_info[possible_sep])
        if 1 == len(keep_seps):
            return keep_seps[0]
        # 如果有多个分隔符分割出的列种类最少，则选择其中列数量最大值最大的那个
        max_sep_num = 0
        for possible_sep in keep_seps:
            if max(possible_sep_info[possible_sep]) > max_sep_num:
                max_sep_num = max(possible_sep_info[possible_sep])
                sep = possible_sep
        return sep

    # 从csv文件读取指定行数
    @staticmethod
    def __read_csv_rows(fn: str, snap_rows: int, encodings: list, sep: str) -> tuple:
        # 按给出编码顺序尝试读取，失败则换下一个编码
        data_buff = []
        final_encoding = encodings[0]
        for each_encoding in encodings:
            try:
                with open(fn, mode='r', encoding=each_encoding) as csv_file:
                    curr_row_idx = 0
                    csv_reader = csv.reader(csv_file,
                                            delimiter=sep,
                                            doublequote=True,
                                            quotechar='"',
                                            skipinitialspace=True,
                                            escapechar=None)
                    max_cols_num = 0
                    for row in csv_reader:
                        data_buff.append(row)
                        max_cols_num = max_cols_num if max_cols_num >= len(row) else len(row)
                        curr_row_idx += 1
                        if curr_row_idx >= snap_rows:
                            break
                final_encoding = each_encoding
                break
            except UnicodeDecodeError as err:
                if each_encoding == encodings[-1]:
                    # 判断的编码不正确，强行尝试的编码也不正确
                    # 只能把错误暴露给上一层了
                    raise err
                continue
        # 返回 csv行、读取的行数、实际使用的编码
        return data_buff, max_cols_num, final_encoding

    # 生成CSV的内容快照
    @staticmethod
    def snapshot_csv(fn: str, snap_rows: int):
        """
        读取csv（含txt后缀名）的文件快照
        :param fn: 需要读取的文件名
        :param snap_rows: 需要读取的快照行数
        :return:
            成功  meta数据dict
            失败  None

            meta数据结构
            {
                'sheet_names_*' : ['工作表名1', '工作表名2', ...],
                '工作表名1' : {
                    'rows' : 快照行数 （不超过快照最大行数）
                    'cols' : 出现在快照中的行中出现的最大列数
                    'snap' : 快照数据，shape为(rows,cols)的nuarray
                },
                '工作表名2' : {
                    ...
                },
                ...
        }
        """
        # 检测文本编码
        encodings = TableMeta.check_txt_encoding(fn)
        if encodings is None:
            return None
        # 检测分隔符
        sep = TableMeta.check_csv_sep(fn, encodings)
        if sep is None:
            return None
        # 读取约定行数的数据
        # noinspection PyBroadException
        try:
            data_buff, max_cols_num, real_encoding = TableMeta.__read_csv_rows(fn, snap_rows, encodings, sep)
        except Exception:
            return None
        # 根据列数最大的行进行扩列
        for row in data_buff:
            if len(row) == max_cols_num:
                # 已经是最大列数，不用扩
                continue
            row.extend([''] * (max_cols_num - len(row)))
        # 生成结果的ndarray
        # noinspection PyBroadException
        try:
            tmp_array = np.array(data_buff)
        except Exception:
            return None
        # 组建 meta dict
        rlst = {'sheet_names_*': ['csv_sheet_*'],
                'encoding': real_encoding,
                'sep': sep,
                'csv_sheet_*': {'rows': len(data_buff),
                                'cols': max_cols_num,
                                'snap': tmp_array}}
        return rlst

    # 匹配两个容器
    @staticmethod
    def __container_match(obj_values: (list, tuple),
                          filters: (list, tuple),
                          size_aligned: bool = False,
                          sequence_aligned: bool = False,
                          min_match_times: (int, type(None)) = None,
                          match_case: bool = True,
                          use_rex: bool = True) -> bool:
        """
        :param obj_values: 将被匹配的数据
        :param filters: 匹配目标数据的过滤器
        :param size_aligned: 容器内容匹配时，是否要求成员数量一致
        :param sequence_aligned: 容器内容匹配时，是否要求顺序一致
        :param min_match_times: 最小匹配次数，小于1或者为None时，认为要求全部匹配
        :param match_case: 是否大小写匹配，默认匹配大小写（True）
        :param use_rex: 是否使用正则匹配，默认使用（True）
        :return:
            匹配    True
            不匹配  False
        """
        if not size_aligned and not sequence_aligned:
            obj_values = list(set(obj_values))
        else:
            obj_values = obj_values.copy() if isinstance(obj_values, list) else list(obj_values)  # cp会有约2%的性能损失
        len_obj = len(obj_values)
        len_filter = len(filters)
        if size_aligned and obj_values != filters:
            # 要求成员数量一致，但传入的目标数据和过滤器大小不一致
            return False
        if not isinstance(min_match_times, int) or min_match_times < 1 or min_match_times > len(filters):
            # 规范化命中次数
            min_match_times = len(filters)
        filters = filters if isinstance(filters, list) else list(filters)
        if len_filter > len_obj and len_obj < min_match_times:
            # 可能命中的匹配次数，无法达到min_match_times
            return False
        match_times = 0
        start_at = 0
        match_flag = re.U if match_case else re.U | re.I
        for item_f in filters:
            # 提取一个filter
            if start_at == len(obj_values):
                # 顺序敏感的场景下，obj_values已经被匹配光了
                break
            valid_obj = obj_values[start_at:] if sequence_aligned else obj_values
            tmp_pattern = re.compile(item_f, match_flag) if isinstance(item_f, str) else None  # 匹配器
            match_at = -1
            for item_o in valid_obj:
                # 用这个filter去匹配所有可以匹配的object_value
                match_at += 1
                if use_rex and isinstance(item_o, str) and isinstance(item_f, str):
                    # 字符串做正则匹配
                    re_match_result = tmp_pattern.match(item_o)
                    if re_match_result is None:
                        # 未匹配
                        continue
                    if len(item_o) != re_match_result.span()[1]:
                        # 只匹配了item_o的一部分，也算不匹配
                        # 如果希望只匹配字符串中的一部分，也要写一个贪婪倾向的正则表达式，将item_o全匹配下来
                        continue
                else:
                    # 非字符串，直接比较
                    if item_f != item_o:
                        continue
                obj_values[start_at + match_at] = NoOneIsMe()  # 被匹配过了就清掉
                match_times += 1  # 命中一个fileter
                if match_times >= min_match_times:
                    return True
                if sequence_aligned:
                    # 如果顺序敏感，item_o被命中一次之后，后面就只在剩下的部分中匹配
                    start_at += match_at + 1
                break
        if match_times < min_match_times:
            return False
        return True
    # endregion

    # region 属性
    """
    """
    # 文件名（含路径）
    @property
    def fn(self) -> str:
        """
        文件名（含路径）
        :return: 文件名（str）
        """
        return self.__fn

    # 文件路径
    @property
    def f_path(self) -> str:
        """
        文件路径
        :return: 文件路径（str）
        """
        return os.path.dirname(self.__fn)

    # 纯文件名
    @property
    def base_name(self) -> str:
        """
        纯文件名
        :return: 纯文件名（str）
        """
        return os.path.basename(self.__fn)

    # 扩展名
    @property
    def ext_name(self) -> str:
        """
        文件扩展名
        :return: 扩展名，不含'.'（str）
        """
        return self.__ext_name

    # 是否是CSV
    @property
    def is_csv(self) -> bool:
        """
        是否是csv文件
        :return:
            是  True
            否  False
        """
        return self.__is_csv

    # 是否是xml
    @property
    def is_xml(self) -> bool:
        return self.__is_xml

    # csv文件编码
    @property
    def encoding(self) -> (str, type(None)):
        """
        csv文件编码
        :return:
            是 csv 文件  编码名称（str）
            非 csv 文件  None
        """
        if self.is_csv:
            return self.__snap['encoding']
        else:
            return None

    # csv文件分隔符
    @property
    def sep(self) -> (str, type(None)):
        """
        csv文件分隔符
        :return:
            是 csv 文件  sep字符（str）
            非 csv 文件  None
        """
        if self.is_csv:
            return self.__snap['sep']
        else:
            return None

    # 所有工作表名称
    @property
    def sheet_names(self):
        """
        获取表格文件所有sheet页的名称的元组
        :return:
        """
        return tuple(self.__snap['sheet_names_*'])

    # 表格文件类型
    @property
    def file_type(self) -> str:
        if self.__is_csv:
            return 'csv'
        elif self.__is_xml:
            return 'xml'
        else:
            return self.ext_name
    # endregion

    # region 成员函数
    """
    """
    # 获取指定工作表的列数
    def sheet_col_num(self, sheet_name: str = None):
        """
        获取指定sheet页的列数量
        :param sheet_name: sheet页名称，如果不提供，则默认取sheet列表里的第一页
        :return:
            指定页存在   sheet页在快照内出现的最大列数
            指定页不存在 None
        """
        if sheet_name is None:
            sheet_name = self.__snap['sheet_names_*'][0]
        elif sheet_name not in self.__snap['sheet_names_*']:
            return None
        return self.__snap[sheet_name]['cols']

    # 获取指定工作表的快照
    def sheet_snap(self, sheet_name: str = None):
        """
        获取指定sheet页数据快照的副本
        :param sheet_name: sheet页名称，如果不提供，则默认取sheet列表里的第一页
        :return: sheet页快照ndarray
                    指定页存在   sheet页快照（ndarray）
                    指定页不存在 None
        """
        if sheet_name is None:
            sheet_name = self.__snap['sheet_names_*'][0]
        elif sheet_name not in self.__snap['sheet_names_*']:
            return None
        return self.__snap[sheet_name]['snap'].copy()

    # 在指定工作表的快照中查找指定的行
    def find_row_in_snap(self,
                         filters: (list, tuple, set),
                         sheet_name: str = None,
                         with_trim: bool = True,
                         size_aligned: bool = False,
                         sequence_aligned: bool = False,
                         min_match_times: (int, type(None)) = None,
                         match_case: bool = True,
                         use_rex: bool = True) -> int:
        """
        根据keys在快照内查找匹配的行
        :param filters: 需要匹配的内容
        :param sheet_name: 查找匹配内容的sheet页
        :param with_trim: 对比字符串内容时，是否忽略两端的空格
        :param size_aligned: 是否要求key的数量与列数量完全一致
        :param sequence_aligned: 是否要求key的顺序与列实际顺序完全一致，该参数当keys为set或dict时将被忽略
        :param min_match_times: 最小匹配次数，小于1或者为None时，认为要求全部匹配
        :param match_case: 是否大小写匹配，默认匹配大小写（True）
        :param use_rex: 是否使用正则匹配，默认使用（True）
        :return:
            找到    第一个匹配行的行号（从0开始）
            没找到  -1
        """
        if sheet_name is None:
            # 不指定sheet页时，默认使用第一个sheet页
            sheet_name = self.__snap['sheet_names_*'][0]
        elif sheet_name not in self.__snap['sheet_names_*']:
            return -1
        sheet_col_num = self.__snap[sheet_name]['cols']
        sheet_snap = self.__snap[sheet_name]['snap']
        if sheet_col_num is None or sheet_snap is None:
            # 根据sheetname提取sheet信息失败
            return -1
        if isinstance(filters, set):
            # 如果keys为set，忽略sequence_aligned参数
            sequence_aligned = False
            filters = list(filters)
        if size_aligned and len(filters) != sheet_col_num:
            # 如果要求列数量对齐，且列数量和keys字段数量不一致，直接返回查找失败
            # 这里有一个默认行为，当表格是CSV时，有些行可能是根据最大列数填充过的，这时候就当作不知道，仍旧严格比较二者列数量
            return -1
        # 遍历每一行，进行匹配
        # 命中第一次匹配后，直接返回对应的行号，不再匹配余下的数据行
        match_at = -1
        for i in range(sheet_snap.shape[0]):
            tmp_row = sheet_snap[i].tolist()
            if with_trim:
                tmp_row = list(map(lambda x: x.strip() if isinstance(x, str) else x, tmp_row))
            if TableMeta.__container_match(tmp_row,
                                           filters,
                                           size_aligned,
                                           sequence_aligned,
                                           min_match_times,
                                           match_case,
                                           use_rex):
                match_at = i
                break
        return match_at
    # endregion


class TableToolkit(object):
    """
    表格文件工具箱
    提供表格文件的统一的读取接口，和并发df处理特性
    """

    # region 重写
    def __new__(cls, fn: str):
        be_self = super(TableToolkit, cls).__new__(cls)
        if be_self is None:
            return None
        meta = TableMeta(fn)
        if meta is None:
            return None
        be_self.__meta = meta
        return be_self

    def __init__(self, fn: str):
        super(TableToolkit, self).__init__()
        self.__orign_fn = fn.strip()
        return
    # endregion

    # region 属性
    """
    """
    # 文件名（含路径）
    @property
    def fn(self) -> str:
        """
        文件名
        :return:
        """
        return self.meta.fn

    # 文件路径
    @property
    def f_path(self) -> str:
        return self.meta.f_path

    @property
    def base_name(self) -> str:
        return self.meta.base_name

    @property
    def ext_name(self) -> str:
        return self.meta.ext_name

    @property
    def sheet_names(self):
        """
        表格文件内所有sheet页的名字
        csv文件也会返回一个特殊的名字
        :return:
        """
        return self.meta.sheet_names

    @property
    def meta(self):
        """
        获取表格文件元数据
        :return:
        """
        return self.__meta
    # endregion

    # region 静态函数
    """
    """
    #
    @staticmethod
    def __check_needed_cols_desc(needed_cols_desc: dict) -> bool:
        """
        用于内部函数__mk_read_params的参数检查
        :param needed_cols_desc: 将被检查是否是一个合法的“要读取的列的描述”
        :return:
            合法  True
            非法  False
        """
        if needed_cols_desc is None:
            return True
        if not isinstance(needed_cols_desc, dict):
            return False
        for k in needed_cols_desc:
            if not isinstance(k, str):
                return False
            if not isinstance(needed_cols_desc[k], (list, tuple)):
                return False
            if 0 == len(needed_cols_desc[k]):
                return False
            if not callable(needed_cols_desc[k][0]):
                return False
            if len(needed_cols_desc[k]) > 1 and not isinstance(needed_cols_desc[k][1], str):
                return False
        return True
    # endregion

    # region 内部函数
    def __mk_read_params(self, sheet_name: str, needed_cols_desc: dict):
        """
        根据对表格文件（excel、csv）的数据需求，生成pandas读取参数
        能够生成的参数包括：
        > usecols
        > names
        > converters
        > header
        :param sheet_name: 要读取的sheet页的名称
        :param needed_cols_desc: 要读取的列的描述信息 {'表格列名': (类型，'df列名')， ...}
        :return:
            成功  读取参数dict，可以**解开直接被 read_csv read_excel 使用，可能为空
                  {
                      'sheet_name': 'sheet name',  # 仅在读取excel时存在
                      'usecols': [x, x, x, x, ...],
                      'names': ['name1', 'name2', ...],
                      'converters': {x:类型, x:类型, ...},
                      'header': x,
                      'sep': '分隔符',  # 仅在读取csv时存在
                      'encoding': '编码名称',  # 仅在读取csv时存在
                      'na_filter': False  # 仅在读取csv时存在
                  }
            失败  None
        """
        # 生成csv文件、excel文件的特有参数
        params = dict()
        if self.meta.is_csv:
            params['sep'] = self.meta.sep
            params['encoding'] = self.meta.encoding
            params['na_filter'] = False
            params['skipinitialspace'] = True
        else:
            params['sheet_name'] = sheet_name
        if not self.__check_needed_cols_desc(needed_cols_desc):
            return None
        if needed_cols_desc is None or 0 == len(needed_cols_desc):
            return params
        # 生成标题行所在行号
        keys = needed_cols_desc.keys()
        header = self.meta.find_row_in_snap(keys,
                                            sheet_name,
                                            size_aligned=False,
                                            sequence_aligned=False,
                                            with_trim=True,
                                            use_rex=False)
        if header < 0:
            return None
        params['header'] = header
        # 生成usecols、converters、names
        usecols = []
        converters = dict()
        names = []
        header_line = self.sheet_snap(sheet_name)[header].tolist()
        needed_cols = needed_cols_desc.keys()
        for idx in range(self.sheet_col_num(sheet_name)):
            curr_col = header_line[idx]  # 每一个列名
            if curr_col not in needed_cols:
                # 如果该列名不被需要，则直接检测下一个
                continue
            curr_cols_num = len(usecols)  # 已经找到的被需要的列的数量
            curr_desc = needed_cols_desc[curr_col]  # 当前被需要列的描述信息
            cvt_type = curr_desc[0]  # 当前描述信息中的converter信息
            if cvt_type is float:
                cvt_type = float_pro
            elif cvt_type is str:
                cvt_type = str_pro
            elif cvt_type is int:
                cvt_type = int_pro
            new_name = curr_desc[1] if len(curr_desc) > 1 else curr_col
            cvt_key = idx if self.meta.is_csv else curr_cols_num  # 当前被需要列，在converter中的idx（csv和excel不一样）
            usecols.append(idx)
            converters[cvt_key] = cvt_type
            names.append(new_name)
        params['usecols'] = usecols
        params['converters'] = converters
        params['names'] = names
        return params
    # endregion

    # region 成员函数
    """
    """
    # 获取工作表列数
    def sheet_col_num(self, sheet_name: str = None):
        """
        获取指定sheet页的列数
        :param sheet_name: sheet页名称，如果不提供，则默认取sheet列表里的第一页
        :return:
            指定页存在   sheet页在快照内出现的最大列数
            指定页不存在 None
        """
        return self.meta.sheet_col_num(sheet_name)

    # 获取工作表快照
    def sheet_snap(self, sheet_name: str = None):
        """
        获取指定sheet页数据快照的副本
        :param sheet_name: sheet页名称，如果不提供，则默认取sheet列表里的第一页
        :return: sheet页快照ndarray
                    指定页存在   sheet页快照（ndarray）
                    指定页不存在 None
        """
        return self.meta.sheet_snap(sheet_name)

    # 读取工作表到DF
    def read_to_df(self, sheet_name: str = None, needed_cols_desc: dict = None, **kwargs):
        """
        读取
        :param sheet_name: 要读取的sheet页的名称，不提供则读取sheet页列表中的第一个
        :param needed_cols_desc: 需要读取的列的描述 {'表格列名': (类型，'df列名')， ...}
        :param kwargs: 其它需要指示给 read_csv/read_excel 的读取参数，如果给定的参数与生成的读取参数重合，则以给定的为准
        :return:
            成功  DF
            失败  None
        """
        # 检测sheet名
        if sheet_name is None:
            sheet_name = self.sheet_names[0]
        elif sheet_name not in self.sheet_names[0]:
            return None
        # 生成读取参数
        params = self.__mk_read_params(sheet_name, needed_cols_desc)
        if params is None:
            return None
        # 如果有额外的读取参数，将其添加（覆盖）到读取参数
        if len(kwargs) > 0:
            for param_name in kwargs:
                params[param_name] = kwargs[param_name]
        if self.meta.is_csv:
            read_func = pd.read_csv
        elif self.meta.is_xml:
            read_func = XMLExcel.directly_read_sheet
        else:
            read_func = pd.read_excel
        # noinspection PyBroadException
        try:
            df = read_func(self.fn, **params)
        except Exception:
            return None
        return df
    # endregion
