#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/1/26 9:28
# @Author: SHAW
# @QQ:838705177
# -----------------------

'''
    One parttern has one parser;
    One parttern has many rules for flaging;
'''

import logging
from .dtrule import KeyMixin

logger = logging.getLogger(__name__)

class DTParttern(object):
    def __init__(self,name,parser,rules,callback=None):
        assert isinstance(rules, (list, tuple, KeyMixin,)), "Rule must be list,tuple,KeyMixin"
        self._name = name
        self._rules = rules
        self._parser = parser
        self.data_callback = callback
        self._pre_code = None

    def pre_code(self,code):
        self._pre_code = code

    def _set_data(self,data):
        if isinstance(data,bytes):
            if self._pre_code=="utf-8" or self._pre_code==None:
                data = data.decode('utf-8','ignore')
            elif self._pre_code=="16bit":
                data = data.hex().upper()
        self._data = data

    def _rule_right(self):
        for keyrule in self._rules:
            if not keyrule.compare(self._data):
                return False
        return True

    def _parse(self):
        return self._parser.parse(self._data)

    def parse_data(self,data):
        self._set_data(data)
        if self._rule_right():
            parsedata = self._parse()
            return parsedata
        else:
            return False

    def parsedata_callback(self,data,stream):
        if self.data_callback:
            self.data_callback(data,stream)

    def __str__(self):
        return "<DtPattern>{}".format(self._name)