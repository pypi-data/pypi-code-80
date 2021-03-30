# -*- coding: utf-8 -*-
# @Time : 2021/3/17
# @Author : NotOne
# @Email : lvsongke@tianyancha.com
import fire
from redisAioSpider.utils.startSpider import runByName


def main():
    fire.Fire(runByName)


if __name__ == '__main__':
    runByName('demo')
