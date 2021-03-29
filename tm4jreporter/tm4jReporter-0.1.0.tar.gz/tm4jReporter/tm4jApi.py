#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: v.stone@163.com


import requests
from pprint import pprint
import os


class Tm4jApi(object):
    def __init__(self, jurl, juser, jpass, jproject, zfolder=None, zplan=None, zcycle=None):
        """
        Init Zephyr Scale API Object
        :param jurl:  Jira URL
        :param juser: Jira Username
        :param jpass: Jira Password
        :param jproject: Jira Project Key
        :param zfolder: Zephyr Scale Test Case Folder
        :param zplan: Zephyr Scale Test Plan Key
        :param zcycle: Zephyr Scale Test Cycle Key
        """
        self.jurl = jurl
        self.juser = juser
        self.jpass = jpass
        self.jproject = jproject
        self.zfolder = zfolder
        self.zplan = zplan
        self.zcycle = zcycle
        self.jauth = (self.juser, self.jpass)
        self.zurl = '%s/rest/atm/1.0' % self.jurl
        self.zfolder = zfolder if zfolder else '/Automation'
        self.zcycle= zcycle if zcycle else os.getenv('TEST_CYCLE_KEY')
        self.session = requests.session()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_environments(self, jira_project=None):
        url = '/'.join([
            self.zurl,
            'environments'
        ])
        query = {
            'projectKey': jira_project if jira_project else self.jproject
        }
        print('GET', url)
        rsp = self.session.get(url=url, auth=self.jauth, headers=self.headers, params=query)
        assert rsp.status_code == 200, '%s\n%s' % (rsp.status_code, rsp.json())
        pprint(rsp.json())
        return rsp.json()

    def post_case(self, case_name, case_folder=None, jira_project=None):
        """
        创建测试用例
        :param case_name:
        :param case_folder:
        :param jira_project:
        :return: caseKey
        """
        url = '/'.join([
            self.zurl,
            'testcase'
        ])
        body = {
            'projectKey': jira_project if jira_project else self.jproject,
            'folder': case_folder if case_folder else self.zfolder,
            'name': case_name,
            'status': 'Approved',
            'labels': ['RobotFramework', 'e2e']
        }
        print('POST', url)
        rsp = self.session.post(url=url, auth=self.jauth, headers=self.headers, json=body)
        assert rsp.status_code == 201, 'Status Code: %s\n%s' % (rsp.status_code, rsp.json())
        return rsp.json()['key']

    def get_case_search(self, case_name, jira_project=None):
        """
        检查测试用例是否存在
        :param case_name:
        :param jira_project:
        :return: caseKey
        """
        url = '/'.join([
            self.zurl,
            'testcase',
            'search'
        ])
        query = {
            'query': ' AND '.join([
                'projectKey = "%s"' % jira_project if jira_project else self.jproject,
                'name = "%s"' % case_name
            ])
        }
        print('GET', url, case_name)
        rsp = self.session.get(url=url, auth=self.jauth, headers=self.headers, params=query)
        assert rsp.status_code == 200, 'Status Code: %s\n%s' % (rsp.status_code, rsp.json())
        if len(rsp.json()) == 0:
            return False
        else:
            return rsp.json()[0]['key']

    def post_case_result(self, test_result, case_key, cycle_key=None):
        """
        上传指定执行的测试结果
        :param test_result:
        :param case_key:
        :param cycle_key:
        :return:
        """
        test_cycle_key = cycle_key if cycle_key else self.zcycle
        assert test_cycle_key, u'cycle_key is required'
        url = '/'.join([
            self.zurl,
            'testrun',
            test_cycle_key,
            'testcase',
            case_key,
            'testresult'
        ])
        body = {
            'status': test_result['status'].capitalize(),
            'environment': test_result['env'],
            'comment': test_result['comment'],
            # 'executedBy': '',
            'executionTime': int((test_result['endtime'] - test_result['starttime']).total_seconds() * 1000),
            'actualStartDate': test_result['starttime'].strftime('%Y-%m-%dT%H:%M:%S+0800'),
            'actualEndDate': test_result['endtime'].strftime('%Y-%m-%dT%H:%M:%S+0800'),
        }
        print('POST', url, case_key)
        rsp = self.session.post(url=url, auth=self.jauth, headers=self.headers, json=body)
        assert rsp.status_code == 201, 'Status Code: %s\n%s' % (rsp.status_code, rsp.json())
        return rsp.json()

    def post_result(self, test_result, case_key, jira_project=None):
        """
        上传一个测试结果
        :param test_result:
        :param case_key:
        :param jira_project:
        :return:
        """
        url = '/'.join([
            self.zurl,
            'testresult'
        ])
        body = {
            'projectKey': jira_project if jira_project else self.jproject,
            'testCaseKey': case_key,
            'status': test_result['status'].capitalize(),
            'environment': test_result['env'],
            'comment': test_result['comment'],
            # 'executedBy': '',
            'executionTime': int((test_result['endtime'] - test_result['starttime']).total_seconds() * 1000),
            'actualStartDate': test_result['starttime'].strftime('%Y-%m-%dT%H:%M:%S+0800'),
            'actualEndDate': test_result['endtime'].strftime('%Y-%m-%dT%H:%M:%S+0800'),
        }
        print('POST', url, case_key)
        rsp = self.session.post(url=url, auth=self.jauth, headers=self.headers, json=body)
        assert rsp.status_code == 201, 'Status Code: %s\n%s' % (rsp.status_code, rsp.json())
        return rsp.json()


if __name__ == '__main__':
    print('This is TM4J API scripts')
