#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
from pprint import pprint
import os
from .tm4jApi import Tm4jApi
from .tm4jParse import parse_robot_output


class Tm4jReporter(object):
    def __init__(self, jira_url, jira_user, jira_pass, jira_project,
                 tm4j_folder=None, tm4j_plan=None, tm4j_cycle=None, tm4j_env=None):
        """
        Init TM4J Reporter
        :param jira_url:
        :param jira_user:
        :param jira_pass:
        :param jira_project:
        :param tm4j_folder:
        :param tm4j_plan:
        :param tm4j_cycle:
        :param tm4j_env:
        """
        self.tm4j = Tm4jApi(
            jurl=jira_url,
            juser=jira_user,
            jpass=jira_pass,
            jproject=jira_project,
            zfolder=tm4j_folder,
            zplan=tm4j_plan,
            zcycle=tm4j_cycle
        )
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def __check_and_create_case_key(self, case_name, case_folder=None, jira_project=None):
        """
        检查用例名称，若不存在则新建一个
        :param case_name:
        :param case_folder:
        :param jira_project:
        :return:
        """
        case_key = self.tm4j.get_case_search(case_name, jira_project)
        if case_key:
            return case_key
        else:
            return self.tm4j.post_case(case_name, case_folder, jira_project)

    def __check_and_create_env(self, env_name, env_desc='', jira_project=None):
        """
        检查环境信息，若不存在则创建
        :param env_name:
        :param env_desc:
        :param jira_project:
        :return:
        """
        envs = list()
        for env in self.tm4j.get_environments(jira_project):
            envs.append(env['name'])
        if env_name not in envs:
            self.tm4j.post_environments(env_name, env_desc, jira_project)
        return env_name

    def __upload_result_to_case(self, test_result, case_key, cycle_key, jira_project=None, run_env=None):
        """
        如果指定 cycleKey 则上传到指定 Cycle，如果未指定 cycleKey 则直接上传结果
        :param test_result:
        :param case_key:
        :param cycle_key:
        :param jira_project:
        :param run_env:
        :return:
        """
        if run_env:
            run_env = self.tm4j.get_environments()
        if cycle_key:
            self.tm4j.post_case_result(test_result, case_key, cycle_key, run_env)
        else:
            self.tm4j.post_result(test_result, case_key, jira_project, run_env)

    def robotframework(self, output_xml_file, cycle_key=None, run_env=None):
        """
        解析 robotframework output.xml 并上传结果到 Zephyr Scale
        :param output_xml_file:
        :param cycle_key:
        :param run_env:
        :return:
        """
        for result in parse_robot_output(output_xml_file):
            self.__upload_result_to_case(
                test_result=result,
                case_key=self.__check_and_create_case_key(result['casename']),
                cycle_key=cycle_key,
                run_env=run_env
            )
            pprint(result)


if __name__ == '__main__':
    print('This is Python scripts')
