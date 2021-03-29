#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import xml.etree.ElementTree as xmlET
from datetime import datetime


def __parse_robot_suite(results, etree, name_prefix=None):
    """
    解析 RobotFramework output.xml 的内容
    :param results: parsed result list
    :param etree: suite root
    :param name_prefix: suite root
    :return:
    """
    _suites = etree.findall('suite')
    if len(_suites) == 0:
        _tests = etree.findall('test')
        for _test in _tests:
            if name_prefix:
                _case_name = '%s.%s' % (name_prefix, _test.get('name'))
            else:
                _case_name = _test.get('name')
            _test_status = _test.findall('status')[0]
            _test_kws = list()
            for _test_kw in _test.findall('kw'):
                _test_kws.append(_test_kw.get('name'))
            results.append({
                'casename': _case_name,
                'status': _test_status.get('status').capitalize(),
                'starttime': datetime.strptime(_test_status.get('starttime').split('.')[0], '%Y%m%d %H:%M:%S'),
                'endtime': datetime.strptime(_test_status.get('endtime').split('.')[0], '%Y%m%d %H:%M:%S'),
                'comment': '<br>'.join(_test_kws),
            })
    else:
        for _suite in _suites:
            if name_prefix:
                _name_prefix = '%s.%s' % (name_prefix, _suite.get('name'))
            else:
                _name_prefix = _suite.get('name')
            __parse_robot_suite(results, _suite, _name_prefix)


def parse_robot_output(output_xml_file):
    robot_results = list()
    __parse_robot_suite(
        results=robot_results,
        etree=xmlET.ElementTree(file=output_xml_file),
        name_prefix=None
    )
    return robot_results


if __name__ == '__main__':
    print('This is parse for TM4J')
