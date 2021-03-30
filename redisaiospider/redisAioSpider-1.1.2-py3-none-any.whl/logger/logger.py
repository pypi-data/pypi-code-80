# -*- coding: utf-8 -*-
# @Time : 2021/1/6
# @Author : NotOne
# @Email : lvsongke@tianyancha.com

import logging
import logging.handlers
import os

from loguru import logger


class Logger():
    def __init__(self):
        pass
        # cur_path = os.path.abspath(os.path.join(os.getcwd(), "."))
        # self.log_path = os.path.join(os.path.dirname(cur_path), 'logs')
        # # 如果不存在这个logs文件夹，就自动创建一个
        # if not os.path.exists(self.log_path):
        #     os.mkdir(self.log_path)

    # def get_logger(self, processPath, debug=True):
    #     fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)s]: %(message)s',
    #                             "%Y-%m-%d %H:%M:%S")
    #     # logging.basicConfig()
    #     logger = logging.getLogger(__name__)
    #     logger.setLevel(logging.INFO)
    #     if debug:
    #         console_handler = logging.StreamHandler()
    #         console_handler.setFormatter(fmt)
    #     proPath = os.path.join(self.log_path, processPath)
    #     if not os.path.exists(proPath):
    #         os.mkdir(proPath)
    #     timefilehandler = logging.handlers.RotatingFileHandler(proPath + '/{}.log'.format(processPath),
    #                                                            maxBytes=1024 * 1024 * 30, backupCount=5,
    #                                                            encoding="utf-8", delay=False)
    #     # timefilehandler.suffix = "%Y-%m-%d.log"
    #     # timefilehandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
    #     timefilehandler.setFormatter(fmt)
    #
    #     if logger.handlers:
    #         return logger
    #     if debug:
    #         logger.addHandler(console_handler)
    #     logger.addHandler(timefilehandler)
    #     return logger

    def get_logger(self, *args):
        return logger


if __name__ == '__main__':
    logger = Logger().get_logger('test')
    logger.info('这是一次测试')
