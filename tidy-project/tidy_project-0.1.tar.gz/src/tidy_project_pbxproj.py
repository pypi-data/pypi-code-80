# -*- coding: utf-8 -*-
"""
扫描整个项目目录结构：
    两个API一个添加目录,一个添加文件
"""
import os
import re

from .conf import NO_SCAN_DIR, NO_SCAN_FILE
from .xcode_helper_v2 import get_project_pbxproj_path, get_parent_name, get_parent_path, XcodeGenerator

GROUP_PATTERN = r'{p_uuid}.*?isa = PBXGroup;\s+children = \((.*?)\);'


def pass_ignore_parent(parent):
    for item in parent.split(os.sep):
        for dir_ in NO_SCAN_DIR:
            if dir_ in item:
                return True


def pass_ignore_dir(dir_):
    for item in NO_SCAN_DIR:
        if item in dir_:
            return True


def pass_ignore_file(file):
    if file in NO_SCAN_FILE:
        return True


class TidyProject:
    def __init__(self, root):
        self.root_path = root
        self.data = ""
        self.uuid_map = {}
        self.no_add_dirs = []
        self.no_add_files = []

    def get_main_group_uuid(self):
        main_group_pattern = re.compile("mainGroup = ([0-9A-E]{24});")
        return main_group_pattern.findall(self.data)[0]

    def get_project_uuid(self):
        pattern = re.compile(r'([0-9A-F]{24}) /\* %s \*/,' % self.project_name)
        res = pattern.findall(self.data, re.S)
        return res[0]

    def get_children(self, parent_uuid):
        res = {}
        gp_children_pattern = re.compile(r'([0-9A-F]{24}) /\* (.*?) \*/,', re.S)
        gp = re.compile(GROUP_PATTERN.format(p_uuid=parent_uuid), re.S)
        for item in gp.findall(self.data):
            for k, v in gp_children_pattern.findall(item):
                res[v] = k
                self.uuid_map[k] = v
        return res

    def get_partition_index(self):
        for parent, _, _ in os.walk(self.root_path):
            if parent.endswith(".xcodeproj"):
                return len(parent.split(os.sep))

    def get_children_by_path(self, path):
        path_lists = path.split(os.sep)[self.partition_index - 1:]
        # 获取project.pbxproj文件中对应path_lists的children
        res = self.get_children(self.project_uuid)
        for i in range(len(path_lists)):
            if i > 0:
                res = self.get_children(res[path_lists[i]])
        return res

    def read_project_pbxproj(self):
        self.read_project_pbxproj_path = get_project_pbxproj_path(self.root_path)
        with open(self.read_project_pbxproj_path, 'r', encoding="utf-8") as f:
            self.data = f.read()

    def pass_no_handle_dir(self, parent):
        for dir_path in self.no_handle_path:
            if dir_path in parent:
                return True

    def scan_diff(self):
        # 读取配置文件存入data中
        self.read_project_pbxproj()
        # 获取项目名称
        self.project_name = get_parent_name(self.root_path)
        self.project_path = get_parent_path(self.root_path)
        # 获取项目的父目录
        self.partition_index = self.get_partition_index()
        # 获取项目的uuid
        self.project_uuid = self.get_project_uuid()
        self.no_handle_path = []
        # 遍历文件比较差异
        for parent, dirs, files in os.walk(self.project_path):
            # 过滤自定义文件夹
            if pass_ignore_parent(parent):
                continue
            # 过滤未添加到project.pbxproj的目录
            if self.pass_no_handle_dir(parent):
                continue
            children_dict = self.get_children_by_path(parent)
            # 对比目录
            for dir_ in dirs:
                if pass_ignore_dir(dir_):
                    continue

                if dir_ in children_dict:
                    continue
                # 记录添加加这个目录,并且在下次扫描时过滤该目录
                dir_path = os.path.join(parent, dir_)
                self.no_add_dirs.append(dir_path)
                self.no_handle_path.append(dir_path)
            # 对比文件
            for file in files:
                file_path = os.path.join(parent, file)
                if pass_ignore_file(file):
                    continue
                if file in children_dict:
                    continue
                # 记录添加加这个目录,并且在下次扫描时过滤该目录
                self.no_add_files.append(file_path)

    # 将no_add_dirs和no_add_files分别添加到文件中
    def add_file_to_project(self):
        xg = XcodeGenerator(self.root_path)
        for dir_path in self.no_add_dirs:
            xg.create_dir(dir_path)
        for file_path in self.no_add_files:
            base_dir, file_name = os.path.split(file_path)
            print(base_dir, file_name)
            xg.create_files(base_dir, [file_name])

    def run(self):
        self.scan_diff()
        self.add_file_to_project()


if __name__ == '__main__':
    tp = TidyProject(r'D:\test1\KWGameJTK')
    tp.run()
    print(tp.no_add_dirs)
    print(tp.no_add_files)
