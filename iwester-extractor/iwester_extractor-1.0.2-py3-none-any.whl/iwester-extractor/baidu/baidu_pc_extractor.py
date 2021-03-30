# -*- coding: utf8 -*-
import os
import re
import sys
import traceback
import urllib.request
import json


class BaiduPcExtractor(object):
    def __init__(self):
        super(BaiduPcExtractor, self).__init__()

    def baidu_pc_extractor(self, body,spidertype=1):
        print('开始解析 百度pc端 列表页')
        rankList = list()
        rankitem['rankList'] = rankList
        return rankitem

if __name__ == '__main__':

    b = BaiduPcExtractor()
    file_path = 'test_pc.html'.format(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    content = open(file_path, 'r', encoding='utf-8')
    html = content.read()
    content.close()

    l_s = b.baidu_pc_extractor(html, spidertype=2)