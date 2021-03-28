# coding = utf-8
# 本程序进行了简单的整数四则运算操作包装
# 对于除法的返回结果进行了优化，可以返回假分数、真分数和带分数或小数
import re
from Basic_Math import Elemental_calculation_decimal as Ecd
class DividedByZeroError(Exception):
    def __init__(self):
        self.__str = '<ERROR> You can\'t divide with zero!'
    def __str__(self):
        print(self.__str)
def add(args_list):
    ret = 0
    round = 0
    for arg in args_list:
        if re.match('[0-9]+\\.[0-9]+', arg) is not None:
            ret = Ecd.add([str(ret), arg], round)
            continue
        ret += int(arg)
    return ret
def minus(arg1, arg2):
    return int(arg1) - int(arg2)
def multiply(args_list):
    ret = 1
    for arg in args_list:
        ret *= int(arg)
    return ret
class division:
    def arg2iszero(self):
        if self.__arg2 == 0:
            raise DividedByZeroError
    def arg1iszero(self):
        if self.__arg1 == 0:
            return 0
    def __init__(self, arg1, arg2):
        self.__arg1 = int(arg1)
        self.__arg2 = int(arg2)
    def div_num(self):
        self.arg2iszero()
        self.arg1iszero()
        return self.__arg1 / self.__arg2
    def div_fra(self):
        self.arg2iszero()
        self.arg1iszero()
        sign = self.__arg1 * self.__arg2
        if self.__arg1 < 0:
            self.__arg1 *= -1
        if self.__arg2 < 0:
            self.__arg2 *= -1
        __mod = self.__arg1 % self.__arg2
        __int = self.__arg1 // self.__arg2
        __fake_upper = __mod + __int * self.__arg2
        __ret = ''
        if sign < 0:
            __ret += '-'
        choice = input('Do you want to print fake fracture or true fracture? input "Y" to get true fracture: ')
        if choice != 'Y' and choice != 'y':
            if __mod != 0:
                __ret += str(__fake_upper) + '/' + str(self.__arg2)
            elif __mod == 0:
                __ret += str(__int)
        else:
            if self.__arg1 > self.__arg2 and __mod != 0:
                __ret += str(__int) + '(' + str(__mod) + '/' + str(self.__arg2) + ')'
            elif self.__arg1 < self.__arg2:
                __ret += str(__mod) + '/' + str(self.__arg2)
            else:
                __ret += str(__int)
        return __ret