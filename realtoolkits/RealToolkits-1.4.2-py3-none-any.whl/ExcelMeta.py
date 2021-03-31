# -*- coding: UTF-8 -*-

import ctypes
import os
import json
import numpy as np
import xlrd
import platform


# 获取get_xlsx_meta_fast需要的动态链接库
def get_dll():
    dll = None
    dll_path = os.path.abspath(os.path.dirname(__file__))
    if 'win' in platform.system().lower():
        # dll = ctypes.CDLL(os.path.join(os.path.abspath('.'), 'RealToolkits', 'excel_meta.dll'))
        dll = ctypes.CDLL(os.path.join(dll_path, 'excel_meta.dll'))
    elif 'linux' in platform.system().lower():
        # dll = ctypes.CDLL(os.path.join(os.path.abspath('.'), 'RealToolkits', 'excel_meta.so'))
        dll = ctypes.CDLL(os.path.join(dll_path, 'excel_meta.so'))
    return dll


# 获取xlsx文件所有工作表名称（按顺序）
def get_xlsx_sheet_names(fn: str, dll=None):
    """
    获取xlsx文件所有工作表名称（按顺序）
    :param fn: excel文件名
    :param dll: 提供真正逻辑实现的dll库，如果不指定，则自行调用get_dll获取
    :return:
    """
    if dll is None:
        dll = get_dll()
    func = dll.GetSheetNames
    func.argtypes = [ctypes.c_char_p]
    func.restype = ctypes.c_char_p
    rlst = func(fn.encode('utf8'))
    return rlst.decode('utf8')


# 获取xlsx文件meta数据
def get_xlsx_meta_fast(fn: str, snap_size: int, dll=None):
    """
    获取xlsx文件的meta数据
        > 工作表名称（按顺序）
        > 每个工作表的 行数、列数、前n行内容（快照）
    :param fn: xlsx文件名（含路径）
    :param snap_size: 需要读取的快照行数
    :param dll: 提供真正逻辑实现的dll库，如果不指定，则自行调用get_dll获取
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
    # 从DLL抽取GetExcelMetaFast函数信息
    if dll is None:
        dll = get_dll()
    func = dll.GetExcelMetaFast
    func.argtypes = [ctypes.c_char_p, ctypes.c_int]
    func.restype = ctypes.c_char_p
    # 调用GetExcelMetaFast函数
    # noinspection PyBroadException
    try:
        rlst = func(fn.encode('utf8'), snap_size)
        if '' == rlst:
            return None
    except Exception:
        return None
    # 将返回的JSON格式meta信息转换成dict
    org_json = json.loads(rlst, encoding='utf8')
    dst_json = dict()
    # 转换org_json dict中的数据到dst_json
    #     > 表名列表，直接拷贝到dst_json
    #     > 快照尺寸，从["cols", "rows"] 转换成 [int, int]，并拆解成两个字段
    #     > 快照，从 []string 转换成 DataFrame
    dst_json['sheet_names_*'] = org_json['sheet_names_*']
    for sheet_name in org_json['sheet_names_*']:
        # 转换 org_json[表名_size]
        rows = int(org_json[sheet_name + '_size'][0])
        cols = int(org_json[sheet_name + '_size'][1])
        dst_json[sheet_name] = dict()
        dst_json[sheet_name]['rows'] = rows
        dst_json[sheet_name]['cols'] = cols
        # 转换 org_json[表名_snapshot] 到ndarray
        tmp_snap = np.array(org_json[sheet_name + '_snapshot'], dtype=str)
        tmp_snap.shape = (rows, cols)
        dst_json[sheet_name]['snap'] = tmp_snap
    return dst_json


# 获取xls文件meta数据
def get_xls_meta(fn: str, snap_size: int):
    """
    获取xls文件的meta数据
        > 工作表名称（按顺序）
        > 每个工作表的 行数、列数、前n行内容（快照）
    :param fn: xls文件名（含路径）
    :param snap_size: 需要读取的快照行数
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
    devnull = open(os.devnull, 'w')  # 用于屏蔽xlrd的告警打印（没啥可看的，也不提示是啥文件）
    dst_json = dict()
    # noinspection PyBroadException
    try:
        # 打开xls工作簿
        encodings = [None, 'GBK', 'utf-8']
        encoding_idx = 0
        wb = None
        while True:
            try:
                if encodings[encoding_idx] is None:
                    wb = xlrd.open_workbook(fn, logfile=devnull)
                else:
                    wb = xlrd.open_workbook(fn, encoding_override=encodings[encoding_idx], logfile=devnull)
            except LookupError as err:
                encoding_idx += 1
                if encoding_idx == len(encodings):
                    raise err
                else:
                    continue
            break
        if wb is None:
            return None
        # 获取工作表名字
        dst_json['sheet_names_*'] = wb.sheet_names()
        # 获取每个工作表的meta数据
        for sheet_name in dst_json['sheet_names_*']:
            data_buff = []
            tmp_sheet = wb.sheet_by_name(sheet_name)
            dst_json[sheet_name] = dict()
            dst_json[sheet_name]['rows'] = min(snap_size, tmp_sheet.nrows)
            dst_json[sheet_name]['cols'] = tmp_sheet.ncols
            # 提取快照数据
            for i in range(dst_json[sheet_name]['rows']):
                row   = tmp_sheet.row_values(i)
                types = tmp_sheet.row_types(i)
                for j in range(dst_json[sheet_name]['cols']):
                    if 3 == types[j]:
                        # 日期时间
                        row[j] = xls_time_to_str(xlrd.xldate_as_tuple(row[j], 0))
                    elif types[j] > 1:
                        # 非空、非字符串
                        row[j] = str(row[j])
                data_buff.append(row)
            # 转换 data_buff 到ndarray
            tmp_snap = np.array(data_buff, dtype=str)
            dst_json[sheet_name]['snap'] = tmp_snap
    except Exception as err:
        print('\n', fn, '\n', err, '\n')
        return None
    finally:
        devnull.close()
    return dst_json


# xlrd读取日期时间类型单元格数据转换为字符串
def xls_time_to_str(dt: tuple):
    """
    xlrd读取日期时间类型单元格数据转换为字符串
    :param dt:
    :return:
    """
    date_str = ''
    time_str = ''
    if dt[0]+dt[1]+dt[2] > 0:
        date_str = '{:04d}-{:02d}-{:02d}'.format(dt[0], dt[1], dt[2])
    if dt[3] + dt[4] + dt[5] > 0:
        time_str = '{:02d}:{:02d}:{:02d}'.format(dt[3], dt[4], dt[5])
    return (date_str+' '+time_str).strip()
