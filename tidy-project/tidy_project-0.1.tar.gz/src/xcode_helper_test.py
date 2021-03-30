# -*- coding:utf-8 -*-
"""
实现添加目录,或者文件自动产生UUID和文件，保证xcode稳定运行
"""

import os
import re

PNG = ".png"
H = ".h"
M = ".m"
PCH = ".pch"
XIB = ".xib"
PLIST = ".plist"
A = ".a"
JSON = ".json"
MM = ".mm"
TXT = ".txt"


class ProjectBase:
    root_path = None

    def write_source(self, pattern=None, new_str=None):
        res = pattern.findall(self.data)
        if res:
            line = res[0]
            data_ = line.replace('\t\t\t);', '{}			);'.format(new_str))
            self.data = self.data.replace(line, data_)

    def done(self, pbxproj_path):
        with open(pbxproj_path, 'w', encoding="utf-8") as f:
            f.write(self.data)


class PBXSourcesBuildPhase(ProjectBase):
    suffix = [".m", ".mm", ".c"]
    base = '				{uuid} /* {file} in Sources */,'

    def __init__(self):
        self.pattern = re.compile(f'isa = {self.__class__.__name__};.*?files = \(.*?\);', re.S)

    def create(self, uuid, file):
        return self.base.format(uuid=uuid, file=file)


class PBXResourcesBuildPhase(ProjectBase):
    suffix = [".png", ".plist", ".xib", ".storyboard", ".json", ".xcassets", ".txt"]
    base = '				{uuid} /* {file} in Resources */,'

    def __init__(self):
        self.pattern = re.compile(f'isa = {self.__class__.__name__};.*?files = \(.*?\);', re.S)

    def create(self, uuid, file):
        return self.base.format(uuid=uuid, file=file)


class PBXFrameworksBuildPhase(ProjectBase):
    suffix = [".tbd", ".framework"]
    base = '				{uuid} /* {file} in Frameworks */,'

    def create(self, uuid, file):
        return self.base.format(uuid=uuid, file=file)


# 构建PBXBuildFile section部分
class PBXBuildFile(ProjectBase):
    suffix = PBXSourcesBuildPhase.suffix + PBXResourcesBuildPhase.suffix + PBXFrameworksBuildPhase
    base = """		{uuid} /* {file} in Resources */ = {isa = PBXBuildFile; fileRef = {fileRef} /* {file} */; };"""

    def create(self, uuid, file, fileRef):
        return self.base.format(uuid=uuid, file=file, fileRef=fileRef)


# 构建PBXFileReference section部分
class PBXFileReference(ProjectBase):
    suffix = PBXBuildFile.suffix.append('.h')
    base = '		{fileRef} /* {file} */ = {{isa = PBXFileReference; lastKnownFileType = {lastKnownFileType}; path = "{file}"; sourceTree = "<group>";}};\n'
    framework = '		{uuid} /* {file} */ = {isa = PBXFileReference; lastKnownFileType = wrapper.framework; name = {file}; path = System/Library/Frameworks/CoreLocation.framework; sourceTree = SDKROOT; };'
    tdb = '		{uuid} /* {file} */ = {isa = PBXFileReference; lastKnownFileType = "sourcecode.text-based-dylib-definition"; name = {file}; path = usr/lib/{file}; sourceTree = SDKROOT; };'
    app = '		{uuid} /* {file} */ = {isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = "{file}"; sourceTree = BUILT_PRODUCTS_DIR; };'
    lastKnownFileTypeMap = {
        ".h": "sourcecode.c.h",
        ".m": "sourcecode.c.objc",
        ".png": "image.png",
        ".xib": "file.xib",
        ".c": "sourcecode.c.c",
        ".mm": "sourcecode.cpp.objcpp",
        ".a": "archive.ar",
        ".plist": "text.plist.xml",
        ".xcassets": "folder.assetcatalog"
    }

    def create(self, uuid, file, fileRef=None):
        _, f_type = os.path.splitext(file)
        if f_type == '.framework':
            return self.framework.format(uuid=uuid, file=file, fileRef=fileRef)
        elif f_type == 'tdb':
            return self.tdb.format(uuid=uuid, file=file)
        elif f_type == "app":
            return self.app.format(uuid=uuid, file=file)
        return self.base.format(uuid=uuid, file=file, fileRef=fileRef,
                                lastKnownFileType=self.lastKnownFileTypeMap[f_type])


class PBXGroup(ProjectBase):
    base = """
		{uuid} /* {name} */ = {{
			isa = PBXGroup;
			children = (
			);
			path = "{name_}";
			sourceTree = "<group>";
		}};
"""
    alone = '				{ref_uuid} /* {file_name} */,\n'
    end = re.compile(r'/\* End PBXGroup section \*/')
    @staticmethod
    def get_dir_pattern(uuid, father_name):
        dir_regex = '\s*{uuid}\s*/\* {father_name} \*/ = {{\s*isa = PBXGroup;\s*children = \(.*?\);'
        dir_pattern = re.compile(re.escape(dir_regex.format(uuid=uuid, father_name=father_name)))
        return dir_pattern

    @staticmethod
    def get_section_dir_str(uuid, name,name_):
        return PBXGroup.base.format(dir_uuid=uuid, dir_name=name,name_=name_)



    def create(self, uuid, name):
        return self.base.format(uuid=uuid, name=name)

def get_uuid_and_dir(path, dir_, name):
    list_ = dir_.split(os.sep)
    usefull_list = None
    for i, v in enumerate(list_):
        if v == name:
            usefull_list = list_[i:]
            break
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        # 找到首个uuid
        uuid = ''
        for index, dir_name in enumerate(usefull_list):
            if index == 1:
                pattern_first = re.compile(r'\s*(\w+)\s*/\* {} \*/ = {{\s*isa = PBXGroup;\s*children = \(.*?\);'.format(re.escape(dir_name)),
                    re.S)
                res = pattern_first.findall(data)
                if res:
                    uuid = res[0]
            pattern_parent = re.compile(r'\s*{uuid}\s*/\* {dir_name} \*/ = {{\s*isa = PBXGroup;\s*children = \((.*?)\);'.format(uuid=uuid,dir_name=re.escape(dir_name)),re.S)
            str_ = pattern_parent.findall(data)[0]
            number = index + 1
            if number <= len(usefull_list) - 1:
                res = re.compile(
                    r'(\w+) /\* {sub_name} \*/,'.format(sub_name=re.escape(usefull_list[index + 1]))).findall(str_)
                if res:
                    uuid = res[0]
        return uuid

def check_chinese(word):
    return re.compile(r'[\u4e00-\u9fa5]+').findall(word)

class XcodeGenerator:
    def __init__(self, path):
        self.path = path
        self.project_path = self.get_project_path()
        self.parent_name = self.get_parent_name()
        self.set_ = None
        self.find_old_uuid()
        self.count = 0

    #  1.找到最大UUID(24位),找出其中需要修改的部分,每次经行+1生成新的UUID
    def uuid_generator(self):
        def dec_hex(str1):  # 十转十六
            a = str(hex(eval(str1)))
            # print('十进制: %s  转换成 十六进制为：%s' % (str1, a))
            return a

        def hex_dec(str2):  # 十六转十
            b = eval(str2)
            # print('十六进制： %s 转换成十进制为：%s:' % (str2, b))
            return b

        head_, ext_ = None, None
        for i, (k, v) in enumerate(zip(self.set_[-1], self.set_[-2])):
            if k != v:
                head_, ext_ = self.set_[-1][:i + 1], self.set_[-1][i + 1:]
                break
        one = int(hex_dec('0x{}'.format(head_))) + int(self.count + 1)
        self.count += 1
        hex_ = dec_hex(str(one)).upper()[2:] + ext_
        if len(hex_) != 24:
            hex_ = '0' + hex_
        return hex_

    # project.pbxproj 找到project.pbxproj的绝对路径
    def get_project_path(self):
        for parent, _, files in os.walk(self.path):
            for file_name in files:
                if file_name == NAME_:
                    return os.path.join(parent, file_name)

    # 找到工程中最大UUID值
    def find_old_uuid(self):
        pattern_ = re.compile(r'[A-Z0-9]{24}')
        # pattern_one = re.compile(r'/\* Begin PBXBuildFile section \*/(.*?)/\* End PBXBuildFile section \*/', re.S)
        # print("self.project_path:", self.project_path)
        with open(self.project_path, 'r', encoding='utf-8') as f:
            data = f.read()
            res = pattern_.findall(data)
            if res:
                self.set_ = sorted(set(res))
                print('最大uuid:', self.set_[-1])
            return self.set_

    #  向project.pbproj文件中插入对应生成代码
    def insert_str_to_project(self, str_, pattern):
        with open(self.project_path, 'r+', encoding='utf-8') as f:
            file_data = ''
            for line in f:
                if pattern.findall(line):
                    line = str_ + line
                file_data += line
            f.seek(0)
            f.truncate()
            f.write(file_data)

    #  生成BASE_PBXBuildFile_SECTION
    def create_BASE_PBXBuildFile_SECTION(self, file_name, f_type):
        ref_uuid = self.uuid_generator()
        uuid = self.uuid_generator()
        new_line = BASE_PBXBuildFile_SECTION.format(uuid=uuid, ref_uuid=ref_uuid,
                                                    sources=SOURCE_MAP[f_type], file_name=file_name)
        return new_line, uuid, ref_uuid

    # 具体写入插入的字符串函数
    def write_source(self, pattern, new_str):
        with open(self.project_path, 'r+', encoding='utf-8') as f:
            data = f.read()
            res = pattern.findall(data)
            if res:
                line = res[0]
                # if '\t\t\t\t);' in line:
                data_ = line.replace('\t\t\t);', '{}			);'.format(new_str))

                # print('data_:', data_)
                data = data.replace(line, data_)
            f.seek(0)
            f.truncate()
            f.write(data)

    # 获取工程中KWGameJTK.xcodeproj的KWGameJTK工程名
    def get_parent_name(self):
        for parent, dirs, files in os.walk(self.path):
            for dir_ in dirs:
                name, ext = os.path.splitext(dir_)
                if '.xcodeproj' == ext:
                    return name

    #   ********************************功能*****************************************
    #  2. 在某个目录下添加文件(在工程和配置文件)
    def create_files(self, dir_path, fileNames):
        """

        :param dir_path:要添加到工程的目录
        :param fileNames:上述dir_path下的文件
        :return:
        """
        if not os.path.exists(dir_path):
            raise IOError('No such path, Can not insert files')
        _, dst_pbxgroup = os.path.split(dir_path)
        # print('dst_pbxgroup:', dst_pbxgroup)
        uuid = get_uuid_and_dir(self.project_path, dir_path, self.parent_name)
        all_str = {}

        BASE_PBXGroup_SECTION_ALONE_PATTERN = re.compile(
            r'\s*%s\s*/\* %s \*/ = {\s*isa = PBXGroup;\s*children = \(.*?\);' % (uuid, re.escape(dst_pbxgroup)),
            re.S)

        for file_name in fileNames:
            name, f_type = os.path.splitext(file_name)
            ref_uuid = None
            uuid = None



    #  3. 在某个目录下插入文件夹
    def create_dir(self, dir_path):
        file_list = []
        dir_list = []
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_names = os.listdir(dir_path)

        # 父级的文件名
        father, name = os.path.split(dir_path)
        _, father_name = os.path.split(father)
        # 用uuid来匹配要插入的段落
        uuid = get_uuid_and_dir(self.project_path, father, self.parent_name)
        # print('father_name:', father_name, 'name:', name)

        # 在父级目录下插入子目录名,例如：4E8A9A502395FDC50067317C /* 单例 */,
        dir_uuid = self.uuid_generator()
        father_sub_str = PBXGroup.alone.format(ref_uuid=dir_uuid, file_name=name)
        self.write_source(PBXGroup.get_dir_pattern(uuid,father_name), father_sub_str)

        # 实现子目录的PBXGroup部分
        # 判断是否是中文,如果是中文，path = ""
        dir_name_ = f'''"{name}"''' if check_chinese(name) else name
        self.insert_str_to_project(PBXGroup.get_section_dir_str(dir_uuid,name,dir_name_), PBXGroup.end)
        for file_ in file_names:
            # 是文件还是文件夹
            if os.path.isfile(os.path.join(dir_path, file_)):
                file_list.append(file_)
            else:
                dir_list.append(file_)
                self.create_dir(os.path.join(dir_path, file_))

        self.create_files(dir_path, file_list)
