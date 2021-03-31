# -*- coding: UTF-8 -*-

import os
import re
import platform
import shutil
if 'win' in platform.system().lower():
    import win32file
    import win32con


# region 文件/目录状态判定
# 判断文件名是否合法
def valid_fn(fn: str) -> bool:
    """
    判断指定的文件名是否是合法文件名
    :param fn: 待判定的文件名
    :return:
        合法  True
        非法  False
    """
    if not isinstance(fn, str) or 0 == len(fn):
        return False
    return True


# 判断文件是否是隐藏文件
def is_hidden(abs_path: str) -> bool:
    """
    判断指定的文件/目录是否是隐藏文件/目录
    :param abs_path: 文件/目录绝对路径
    :return:
        是隐藏文件    True
        不是隐藏文件  False
    """
    # 检查：
    #    是否是文件名
    #    是否是绝对路径
    #    是否存在
    if not (isinstance(abs_path, str) and os.path.isabs(abs_path) and os.path.exists(abs_path)):
        return False
    # 只有windows平台才存在隐藏文件
    if 'win' not in platform.system().lower():
        return False
    # 直接通过为win32API来读取文件是否具有系统属性
    return (win32file.GetFileAttributesW(abs_path) & win32con.FILE_ATTRIBUTE_HIDDEN) > 0


# 判断文件是否是系统文件
def is_system(abs_path: str) -> bool:
    """
    判断指定的文件/目录是否是系统文件/目录
    :param abs_path: 文件/目录绝对路径
    :return:
        是系统文件    True
        不是系统文件  False
    """
    # 检查：
    #    是否是文件名
    #    是否是绝对路径
    #    是否存在
    if not (isinstance(abs_path, str) and os.path.isabs(abs_path) and os.path.exists(abs_path)):
        return False
    # 只有windows平台才存在隐藏文件
    if 'win' in platform.system().lower():
        # 通过为win32API来读取文件是否具有系统属性
        return (win32file.GetFileAttributesW(abs_path) & win32con.FILE_ATTRIBUTE_SYSTEM) > 0
    else:
        # linux操作系统下，系统文件首字符为 '.'
        return '.' == os.path.basename(abs_path)[:1]
# endregion


# region 文件/目录搜索
def get_all_files(root_path: str,
                  need_file: bool = True,
                  need_folder: bool = True,
                  ext_filter: (str, list, tuple, set, type(None)) = None,
                  keep_hidden: bool = False,
                  keep_system: bool = False) -> (dict, type(None)):
    """
    获取指定路径下指定扩展名的所有文件信息
    如果文件重名，则记录重名文件的路径，并增加一个重名数量
        > 遇子目录递归
        > 剔除隐藏文件和系统文件
    :param root_path: 需要遍历的起始目录
    :param need_file: 是否列出文件， True 是， False 否
    :param need_folder: 是否列出目录， True 是， False 否
    :param ext_filter: 文件的扩展名，可以是逗号分隔的字符串，也可以是list like或者set，传None值按[]处理，该参数仅对文件起作用
    :param keep_system: 结果中是否保留系统文件， True 保留， False 不保留
    :param keep_hidden: 结果中是否保留隐藏文件， True 保留， False 不保留
    :return:
        成功 {纯文件名: {绝对路径1: {'type': 类别（文件 or 目录）, 'attrib': 属性}, ...}
        失败 None
    """
    # 参数类型检查
    if not isinstance(root_path, str):
        return None
    root_path = os.path.abspath(root_path)  # 是不是绝对路径，都先强制转一下
    if not os.path.isdir(root_path):
        return None
    if ext_filter is not None and not isinstance(ext_filter, (str, list, tuple, set)):
        return None
    if not isinstance(need_file, bool):
        return None
    if not isinstance(need_folder, bool):
        return None
    if not isinstance(keep_hidden, bool):
        return None
    if not isinstance(keep_system, bool):
        return None
    # 扩展名过滤参数，统一转成set
    ext_filter = [] if ext_filter is None else ext_filter
    if isinstance(ext_filter, str):
        # 如果ext_filter是字符串，首先转成list like
        ext_filter = ext_filter.split(',')
    std_types = set()
    for a_type in ext_filter:
        a_type = a_type.strip().lower()
        if '' != a_type:
            # 规范化每一个类型名称
            std_types.add(a_type)
    ext_filter = std_types
    # 遍历root_path下所有文件/目录
    all_files = {}
    for pure_path, ds, fs in os.walk(root_path):
        if need_folder:
            # 如果结果中保留目录
            for tmp_fn in ds:
                full_name = os.path.join(pure_path, tmp_fn)
                # 属性过滤
                in_hidden = is_hidden(full_name)
                in_system = is_system(full_name)
                if not keep_hidden and in_hidden:
                    continue
                if not keep_system and in_system:
                    continue
                # 存储目录信息
                att = 'h' if in_hidden else '' + 's' if in_system else ''
                if tmp_fn in all_files:
                    # 如果重名了，将文件路径、类型添加到已有文件名的path列表中
                    all_files[tmp_fn][pure_path] = {'type': 'd', 'attrib': att}
                else:
                    # 如果文件名还没有出现过，创建这个文件的信息
                    all_files[tmp_fn] = {pure_path: {'type': 'd', 'attrib': att}}
        if need_file:
            # 如果结果中保留文件
            for tmp_fn in fs:
                full_name = os.path.join(pure_path, tmp_fn)
                # 属性过滤
                in_hidden = is_hidden(full_name)
                in_system = is_system(full_name)
                if not keep_hidden and in_hidden:
                    continue
                if not keep_system and in_system:
                    continue
                # 扩展名过滤
                if len(ext_filter) > 0:
                    ext_name = os.path.splitext(tmp_fn)[1]
                    if '' == ext_name and '.' == tmp_fn[0] and 'win' in platform.system().lower():
                        # windows环境下 ".csv" 应拆解为 ['', '.']
                        # 特殊处理这种情况
                        ext_name = os.path.splitext('a'+tmp_fn)[1]
                    ext_name = ext_name[1:] if len(ext_name) > 0 else ext_name
                    if ext_name not in ext_filter:
                        # 扩展名不满足过滤条件
                        continue
                # 存储文件信息
                att = 'h' if in_hidden else '' + 's' if in_system else ''
                if tmp_fn in all_files:
                    # 如果重名了，将文件路径、类型添加到已有文件名的path列表中
                    all_files[tmp_fn][pure_path] = {'type': 'f', 'attrib': att}
                else:
                    # 如果文件名还没有出现过，创建这个文件的信息
                    all_files[tmp_fn] = {pure_path: {'type': 'f', 'attrib': att}}
    # 返回所有存在的文件信息
    return all_files


def __check_find_param(root_path: str,
                       dst_name: str,
                       match_case: (bool, type(None)) = False,
                       find_file: bool = True,
                       find_folder: bool = True,
                       find_hidden: bool = False,
                       find_system: bool = False) -> bool:
    if not isinstance(root_path, str):
        return False
    if not isinstance(dst_name, str):
        return False
    if not isinstance(find_file, bool):
        return False
    if not isinstance(find_folder, bool):
        return False
    if not isinstance(find_hidden, bool):
        return False
    if not isinstance(find_system, bool):
        return False
    if not isinstance(match_case, (bool, type(None))):
        return False
    return True


def __find_in_path(just_one: bool,
                   root_path: str,
                   dst_name: str,
                   match_case: (bool, type(None)) = False,
                   find_file: bool = True,
                   find_folder: bool = True,
                   find_hidden: bool = False,
                   find_system: bool = False) -> dict:
    # 参数检查
    if not __check_find_param(root_path, dst_name, match_case, find_file, find_folder, find_hidden, find_system):
        return dict()
    # 参数整理
    root_path = os.path.abspath(root_path)
    if not os.path.isdir(root_path):
        return dict()
    if match_case is None:
        match_case = False if 'win' in platform.system().lower() else True

    # 获取属性满足条件的全部文件/目录
    files = get_all_files(root_path=root_path,
                          need_file=find_file,
                          need_folder=find_folder,
                          ext_filter=None,
                          keep_hidden=find_hidden,
                          keep_system=find_system)
    # 文件名正则匹配
    match_flag = re.U if match_case else re.U | re.I
    tmp_pattern = re.compile(dst_name, match_flag)
    invalid_fn = set()
    for each_fn in files:
        re_match_result = tmp_pattern.match(each_fn)
        if re_match_result is None or len(each_fn) != re_match_result.span()[1]:
            # 如果文件名不匹配，记录下来
            invalid_fn.add(each_fn)
        elif just_one:
            # 如果文件名匹配，并且只需要一个结果
            for first_path in files[each_fn]:
                # 提取第一个满足条件的文件名下面的第一个路径，谁排在前面取决于dict的实现
                return {each_fn: {first_path: files[each_fn][first_path]}}
    # 提取最终结果
    for each_fn in invalid_fn:
        del files[each_fn]
    return files


# 在指定路径下查找一个名字满足要求的文件/目录
def find_one_in_path(root_path: str,
                     dst_name: str = r'[\s\S]+',
                     match_case: (bool, type(None)) = False,
                     find_file: bool = True,
                     find_folder: bool = True,
                     find_hidden: bool = False,
                     find_system: bool = False) -> dict:
    """
    在指定路径下查找名字满足要求的文件/目录，遇到第一个满足条件的文件/目录立刻返回
    :param root_path: 搜索起始的根路径
    :param dst_name: 需要查找的文件名，支持正则表达式
    :param match_case: 是否大小写敏感， 是 True， 否 False，为None时自适应（windows下不敏感，其它敏感）
    :param find_file: 是否查找满足条件的文件， True 是， False 否
    :param find_folder: 是否查找满足条件的目录， True 是， False 否
    :param find_hidden: 是否查找隐藏文件/目录， True 是， False 否
    :param find_system: 是否查找系统文件/目录， True 是， False 否
    :return: 查找结果
        找到    {匹配的文件名: {绝对路径1: {'type': 类别（文件 or 目录）, 'attrib': 属性}, ...}
        未找到  {}
    """
    find_result = __find_in_path(just_one=True,
                                 root_path=root_path,
                                 dst_name=dst_name,
                                 match_case=match_case,
                                 find_file=find_file,
                                 find_folder=find_folder,
                                 find_hidden=find_hidden,
                                 find_system=find_system)
    return find_result


# 在指定路径下查找名字满足要求的所有文件/目录
def find_all_in_path(root_path: str,
                     dst_name: str = r'[\s\S]+',
                     match_case: (bool, type(None)) = False,
                     find_file: bool = True,
                     find_folder: bool = True,
                     find_hidden: bool = False,
                     find_system: bool = False) -> dict:
    """
    在指定目录root_path下查找文件/目录dst_name
    :param root_path: 查找起始的根路径
    :param dst_name: 查找的目标名称，不能带有路径，支持正则表达式
    :param match_case: 是否大小写敏感， 是 True， 否 False，为None时自适应（windows下不敏感，其它敏感）
    :param find_file: 是否查找满足条件的文件， True 是， False 否
    :param find_folder: 是否查找满足条件的目录， True 是， False 否
    :param find_hidden: 是否查找隐藏文件/目录， True 是， False 否
    :param find_system: 是否查找系统文件/目录， True 是， False 否
    :return: 查找结果
        找到    {匹配的文件名: {绝对路径1: {'type': 类别（文件 or 目录）, 'attrib': 属性}, ...}
        未找到  {}
    """
    find_result = __find_in_path(just_one=False,
                                 root_path=root_path,
                                 dst_name=dst_name,
                                 match_case=match_case,
                                 find_file=find_file,
                                 find_folder=find_folder,
                                 find_hidden=find_hidden,
                                 find_system=find_system)
    return find_result
# endregion


# region 文件操作
def empty_folder_ensure(path: str):
    """
    确保指定的目录存在且为空：如果名为path的目录/文件已经存在，则将其删除然后重建名为path的目录
    :param path:  需要重置目录名称（确保该目录）
    :return:
        成功  True, 'ok'
        失败  False, '失败原因'
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        os.makedirs(path)
    except Exception as err:
        return False, '重置目录 {} 失败：{}'.format(path, err)
    return True, 'ok'
# endregion
