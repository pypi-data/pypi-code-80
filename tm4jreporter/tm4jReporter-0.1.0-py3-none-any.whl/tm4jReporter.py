#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
from pprint import pprint
import os
from .tm4jApi import Tm4jApi
from .tm4jParse import parse_robot_output


class Tm4jReporter(object):
    def __init__(self, jira_url, jira_user, jira_pass, jira_project, tm4j_folder=None, tm4j_plan=None, tm4j_cycle=None):
        self.tm4j = Tm4jApi(jira_url, jira_pass, jira_project, tm4j_folder, tm4j_plan, tm4j_cycle)
        self.jira_url = jira_url
        self.jira_user = jira_user
        self.jira_pass = jira_pass
        self.jira_auth = (self.jira_user, self.jira_pass)
        self.tm4j_api_url = '%s/rest/atm/1.0' % self.jira_url
        self.tm4j_folder = '/Automation'
        self.tm4j_cycle = os.getenv('TEST_CYCLE_KEY')
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.project = jira_project

    def __check_and_create_case_key(self, case_name, case_folder=None, jira_project=None):
        case_key = self.tm4j.get_case_search(case_name, jira_project)
        if case_key:
            return case_key
        else:
            return self.tm4j.post_case(case_name, case_folder, jira_project)

    def __upload_result_to_case(self, test_result, case_key, cycle_key, jira_project=None):
        if cycle_key:
            self.tm4j.post_case_result(test_result, case_key, cycle_key)
        else:
            self.tm4j.post_result(test_result, case_key, jira_project)

    def robotframework(self, output_xml_file, cycle_key=None):
        """
        解析 robotframework output.xml 并上传结果到 Zephyr Scale
        :param output_xml_file:
        :param cycle_key:
        :return:
        """
        for result in parse_robot_output(output_xml_file):
            self.__upload_result_to_case(
                test_result=result,
                case_key=self.__check_and_create_case_key(result['case_name']),
                cycle_key=cycle_key
            )
            pprint(result)


if __name__ == '__main__':
    print('This is Python scripts')
