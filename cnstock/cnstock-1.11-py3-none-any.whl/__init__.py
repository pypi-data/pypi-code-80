"""
作者：xjxfly
邮箱：xjxfly@qq.com

说明：
这是基础包，是一些通用功能（纯函数）的集合。
包内提供了一些接口，具体有哪些接口可用及怎样调用，请用 help(包名)  查看，
如果导入包时有 as 过的话，则用 help(as过后的别名) 查看。

"""
# -----------------------------
# 定义可以暴露给外部的接口，必须放在 __all__ 中，且外部只有用 from import 引用时才有效，直接 import 的话，这里的 __all__ 不起作用。；
# 另外，python 内置函数 help() 调用包或模块时，如果模块或包内有 __all__，则只返回 __all__ 中列出的接口的使用方法；否则返回全部接口的使用方法。 
# 这句既是给 from import 看的，也是给内置函数 help() 看的
# 另外 PEP8 建议把 __all__ 放在模块注释后，放在除 from future 之外的其他 import 前


__version__ = '1.11'
__author__ = 'xjxfly'

from .cnstock_lib import *

__all__ = get_api_list()