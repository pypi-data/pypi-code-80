# coding = utf-8
# 本程序进行了简单的小数四则运算操作包装
# 对于除法的返回结果进行了优化，可以返回假分数、真分数和带分数或小数
from Basic_Math import Elemental_calculation_integer as Eci
from math import *
import re
def add(args_list, round_all):
    rnd_list = [0, 0]
    if len(args_list[0].split('.')) == 2:
        rnd_list[0] = len(args_list[0].split('.')[1])
    if len(args_list[1].split('.')) == 2:
        rnd_list[1] = len(args_list[1].split('.')[1])
    round_all = max(rnd_list)
    return round(float(args_list[0]) + float(args_list[1]), round_all)