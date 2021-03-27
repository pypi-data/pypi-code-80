# @Time     : 2021/3/25
# @Project  : w8_auto_utils
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import time
import enum

from w8_auto_py.typings import NumberTypes
from w8_auto_py.global_vars import TimeUnit
from w8_auto_py.common.qps import AbstractQpsTimer


class TimeoutStates(enum.Enum):
    """
    超时状态
    """
    TIMEOUT = 1
    UN_TIMEOUT = -1


class QpsTimer(AbstractQpsTimer):

    def __init__(self, date_unit: TimeUnit):
        self.__date_unit = date_unit
        self.__state: TimeoutStates = TimeoutStates.UN_TIMEOUT

    @property
    def is_timeout(self) -> bool:
        return self.__state == TimeoutStates.TIMEOUT

    def get_current(self) -> NumberTypes:
        """
        获取当前时间
        Returns:

        """
        date_unit = self.__date_unit.value

        if not date_unit:
            date_unit = 10 ** -3

        return int(round(time.time() / date_unit))

    def set_timeout(self) -> None:
        """
        设置超时
        Returns:

        """
        self.__state = TimeoutStates.TIMEOUT

    def clear(self) -> None:
        """
        清除超时
        Returns:

        """
        self.__state = TimeoutStates.UN_TIMEOUT
