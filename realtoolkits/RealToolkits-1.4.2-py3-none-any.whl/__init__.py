# -*- coding: UTF-8 -*-

from .realDecorator import show_time_cost
from .realTblToolkits import TableToolkit, TableMeta, XMLExcel
from .realFileToolkits import is_system, is_hidden, valid_fn
from .realFileToolkits import get_all_files, find_one_in_path, find_all_in_path, empty_folder_ensure
from .type_kits import RealLL, str_pro, int_pro, float_pro, NoOneIsMe, is_number
from .realDistrabutedLock import RealDLock


def ver():
    return '1.4.2'


"""
文档说明：
v1.4.2 整理成发布包，添加安装、版权、readme，dll文件的检索改为到 ExeclMeta.py文件所在路径寻找
v1.4.1 优化了realFileTookits，用 get_all_files+文件名正则表达式匹配 重新实现了 find_all_in_path 和 find_one_in_path
v1.4.0 增加了分布式锁
v1.3.0 在type_kits中增加了双向链表RealLL，并实现了merge sort，quick/tim/heap未实现
v1.2.1 将ExcelMeta暴露到接口，以支持多进程调用realTblToolkits
       之前dll的导入是在ExcelMeta的全局变量中导入的，在linux环境下无法正常工作在多进程模式
v1.2.0 为realTblToolkits增加了对XML格式表格的支持
       为realTblToolkits增加了对表格行进行正则表达式匹配的能力（源于需要寻找非标准流水的标题行）
v1.1.0 实现realFileToolkits，实现对文件的遍历、查找功能
v1.0.0 实现realTblToolkits，提供对excel/csv文件的快照、读取功能
"""
