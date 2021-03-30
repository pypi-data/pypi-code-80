# -*- coding:utf-8 -*-
"""
实现添加目录,或者文件自动产生UUID和文件，保证xcode稳定运行\
比较xcode_helper,添加了xml,plist,json等文件类型的添加
"""

import os
import re

# 1/* Begin PBXBuildFile section */ 下的.m 文件或者.png 4E8A9ADF2395FDC50067317C>4E8A9A4B2395FDC50067317C
BASE_PBXBuildFile_SECTION = "		{uuid} /* {file_name} in {sources} */ = {{isa = PBXBuildFile; fileRef = " \
                            "{ref_uuid} /* {file_name} */; }};\n"

# 2/* Begin PBXFileReference section */ 包含.png, .h, .m文件
# 2.1 如果为图片：
#   4E8A99E42395FDC50067317C /* FeeConsent@3x.png */ = {isa = PBXFileReference;
#   lastKnownFileType = image.png; path = "FeeConsent@3x.png"; sourceTree = "<group>"; };

#   4E8A99F72395FDC50067317C /* KWZQBaHeHeTool.h */ = {isa = PBXFileReference;
#   fileEncoding = 4; lastKnownFileType = sourcecode.c.h; path = KWZQBaHeHeTool.h; sourceTree = "<group>"; };

#   4E8A99F82395FDC50067317C /* KWZQBaHeHeTool.m */ = {isa = PBXFileReference;
#   fileEncoding = 4; lastKnownFileType = sourcecode.c.objc; path = KWZQBaHeHeTool.m; sourceTree = "<group>"; };

BASE_PBXFileReference_SECTION_PIC = '		{ref_uuid} /* {file_name} */ = ' \
                                    '{{isa = PBXFileReference; lastKnownFileType = image.png; path = "{file_name}"; ' \
                                    'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_H = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                  ' fileEncoding = 4; lastKnownFileType = sourcecode.c.h; path = "{file_name}"; ' \
                                  'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_M = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                  ' fileEncoding = 4; lastKnownFileType = sourcecode.c.objc; path = "{file_name}"; ' \
                                  'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_XIB = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                    ' fileEncoding = 4; lastKnownFileType = file.xib; path = "{file_name}"; ' \
                                    'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_C = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                  ' fileEncoding = 4; lastKnownFileType = sourcecode.c.c; path = "{file_name}"; ' \
                                  'sourceTree = "<group>"; }};\n'
BASE_PBXFileReference_SECTION_MM = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                   ' fileEncoding = 4; lastKnownFileType = sourcecode.cpp.objcpp; path = "{file_name}"; ' \
                                   'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_JSON = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                     ' fileEncoding = 4; lastKnownFileType = text.json; path = "{file_name}"; ' \
                                     'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_PLIST = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                      ' fileEncoding = 4; lastKnownFileType = text.plist.xml; path = "{file_name}"; ' \
                                      'sourceTree = "<group>"; }};\n'

BASE_PBXFileReference_SECTION_TXT = '		{ref_uuid} /* {file_name} */ = {{isa = PBXFileReference;' \
                                    ' fileEncoding = 4; lastKnownFileType = text.txt; path = "{file_name}"; ' \
                                    'sourceTree = "<group>"; }};\n'

# 3. /* Begin PBXGroup section */
BASE_PBXGroup_SECTION_ALONE = '				{ref_uuid} /* {file_name} */,\n'
BASE_PBXGroup_SECTION_DIR = """
		{dir_uuid} /* {dir_name} */ = {{
			isa = PBXGroup;
			children = (
			);
			path = {dir_name_};
			sourceTree = "<group>";
		}};
"""
BASE_PBXGroup_SECTION_PATTERN = re.compile(r'/\* End PBXGroup section \*/')

# 4. /* Begin PBXSources|Resources BuildPhase section */ 该部分包括Sources(.m文件) 和 Resources(.xib,.png文件) 两部分资源
BASE_PBXBuildPhase_SECTION = '				{uuid} /* {file_name} in {source} */,\n'

BASE_PBXResourceBuildPhase_SECTION_PATTERN = re.compile(
    r'\s*\w+\s*/\* Resources \*/ = {\s*isa = PBXResourcesBuildPhase;.*?files = \(.*?\);', re.S)

BASE_PBXSourceBuildPhase_SECTION_PATTERN = re.compile(
    r'\s*\w+\s*/\* Sources \*/ = {\s*isa = PBXSourcesBuildPhase;.*?files = \(.*?\);', re.S)

NAME_ = 'project.pbxproj'
BASE_PBXBuildFile_SECTION_PATTERN = re.compile(r'/\* End PBXBuildFile section \*/')
BASE_PBXFileReference_SECTION_PATTERN = re.compile(r'/\* End PBXFileReference section \*/')

SUFFIX_MAP = {
    '.png': BASE_PBXFileReference_SECTION_PIC,
    '.h': BASE_PBXFileReference_SECTION_H,
    '.m': BASE_PBXFileReference_SECTION_M,
    '.c': BASE_PBXFileReference_SECTION_C,
    '.xib': BASE_PBXFileReference_SECTION_XIB,
    '.mm': BASE_PBXFileReference_SECTION_MM,
    '.json': BASE_PBXFileReference_SECTION_JSON,
    '.plsit': BASE_PBXFileReference_SECTION_PLIST,
    '.txt': BASE_PBXFileReference_SECTION_TXT
}
SOURCES = ['.m', '.mm', '.c']
RESOURCES = [".png", ".xib", ".txt", ".json", ".plist"]
SOURCE_MAP = {
    '.m': 'Sources',
    '.mm': 'Sources',
    '.c': 'Sources',

    '.png': 'Resources',
    '.xib': 'Resources',
    '.plist': 'Resources',
    '.json': 'Resources',
    '.txt': 'Resources',
}


def check_chinese(word):
    return re.compile(r'[\u4e00-\u9fa5]+').findall(word)


def get_uuid_and_dir(path, dir_, name):
    list_ = dir_.split('\\')
    usefull_list = None
    for i, v in enumerate(list_):
        if v == name:
            usefull_list = list_[i:]
            break
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        # 找到首个uuid
        uuid = ''
        # print('name:', name)

        for index, dir_name in enumerate(usefull_list):
            # print("dir_name:", dir_name,"index:",index)
            if index == 1:
                # if index == 0:
                pattern_first = re.compile(
                    r'\s*(\w+)\s*/\* {} \*/ = {{\s*isa = PBXGroup;\s*children = \(.*?\);'.format(re.escape(dir_name)),
                    re.S)
                # print("pattern_first:", pattern_first)
                # uuid = pattern_first.findall(data)[0]
                res = pattern_first.findall(data)
                if res:
                    uuid = res[0]
                # str_ = pattern_first.findall(data)[1]

            pattern_parent = re.compile(
                r'\s*{uuid}\s*/\* {dir_name} \*/ = {{\s*isa = PBXGroup;\s*children = \((.*?)\);'.format(uuid=uuid,
                                                                                                        dir_name=re.escape(
                                                                                                            dir_name)),
                re.S)
            # print("pattern_parent:", pattern_parent)
            str_ = pattern_parent.findall(data)[0]
            # print('str_:', str_)
            number = index + 1
            if number <= len(usefull_list) - 1:
                res = re.compile(
                    r'(\w+) /\* {sub_name} \*/,'.format(sub_name=re.escape(usefull_list[index + 1]))).findall(str_)
                if res:
                    uuid = res[0]
                # print('uuid', uuid)
        return uuid


# 获取工程中KWGameJTK.xcodeproj的KWGameJTK工程名
def get_parent_name(path):
    for parent, dirs, files in os.walk(path):
        for dir_ in dirs:
            name, ext = os.path.splitext(dir_)
            if '.xcodeproj' == ext:
                return name


def get_parent_path(path):
    for parent, dirs, files in os.walk(path):
        for dir_ in dirs:
            name, ext = os.path.splitext(dir_)
            if '.xcodeproj' == ext:
                return os.path.join(parent, name)


# project.pbxproj 找到project.pbxproj的绝对路径
def get_project_pbxproj_path(path):
    for parent, _, files in os.walk(path):
        for file_name in files:
            if file_name == NAME_:
                return os.path.join(parent, file_name)


#   生成create_BASE_PBXFileReference_SECTION
def create_BASE_PBXFileReference_SECTION(file_name, ref_uuid, model_str):
    return model_str.format(file_name=file_name, ref_uuid=ref_uuid)


class XcodeGenerator:

    def __init__(self, path):
        self.path = path
        self.project_path = get_project_pbxproj_path(path)
        self.parent_name = get_parent_name(path)
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
        BASE_PBXBuildFile_SECTION_STR = ''
        BASE_PBXFileReference_SECTION_STR = ''
        BASE_PBXGroup_SECTION_ALONE_STR = ''
        BASE_PBXSourceBuildPhase_SECTION_STR = ''
        BASE_PBXResourceBuildPhase_SECTION_STR = ''
        BASE_PBXGroup_SECTION_ALONE_PATTERN = re.compile(
            r'\s*%s\s*/\* %s \*/ = {\s*isa = PBXGroup;\s*children = \(.*?\);' % (uuid, re.escape(dst_pbxgroup)), re.S)

        for file_name in fileNames:
            name, f_type = os.path.splitext(file_name)
            ref_uuid = None
            uuid = None

            if f_type in SOURCE_MAP:
                PBXBuildFile_Str, uuid, ref_uuid = self.create_BASE_PBXBuildFile_SECTION(file_name, f_type)
                BASE_PBXBuildFile_SECTION_STR += PBXBuildFile_Str

            if f_type in SUFFIX_MAP:  # 根据文件后缀选择相应模版
                if not ref_uuid:
                    ref_uuid = self.uuid_generator()
                BASE_PBXFileReference_SECTION_STR += create_BASE_PBXFileReference_SECTION(file_name, ref_uuid,
                                                                                          SUFFIX_MAP[f_type])

            # 插入Begin PBXGroup section 部分
            BASE_PBXGroup_SECTION_ALONE_STR += BASE_PBXGroup_SECTION_ALONE.format(ref_uuid=ref_uuid,
                                                                                  file_name=file_name)
            # 插入 Begin PBXSources|Resources BuildPhase section 部分
            if f_type in SOURCE_MAP:

                # uuid = uuid if uuid else self.uuid_generator()
                if f_type in SOURCES:
                    BASE_PBXSourceBuildPhase_SECTION_STR += BASE_PBXBuildPhase_SECTION.format(
                        uuid=uuid, file_name=file_name, source="Sources")
                if f_type in RESOURCES:
                    BASE_PBXResourceBuildPhase_SECTION_STR += BASE_PBXBuildPhase_SECTION.format(
                        uuid=uuid, file_name=file_name, source="Resources")

        if BASE_PBXResourceBuildPhase_SECTION_STR:
            self.write_source(BASE_PBXResourceBuildPhase_SECTION_PATTERN, BASE_PBXResourceBuildPhase_SECTION_STR)

        if BASE_PBXSourceBuildPhase_SECTION_STR:
            self.write_source(BASE_PBXSourceBuildPhase_SECTION_PATTERN, BASE_PBXSourceBuildPhase_SECTION_STR)

        if BASE_PBXGroup_SECTION_ALONE_STR:
            self.write_source(BASE_PBXGroup_SECTION_ALONE_PATTERN, BASE_PBXGroup_SECTION_ALONE_STR)

        all_str[BASE_PBXBuildFile_SECTION_STR] = BASE_PBXBuildFile_SECTION_PATTERN
        all_str[BASE_PBXFileReference_SECTION_STR] = BASE_PBXFileReference_SECTION_PATTERN
        for str_, pattern_ in all_str.items():
            self.insert_str_to_project(str_, pattern_)

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

        BASE_PBXGroup_SECTION_DIR_PATTERN = re.compile(
            r'\s*{uuid}\s*/\* {father_name} \*/ = {{\s*isa = PBXGroup;\s*children = \(.*?\);'.format(
                uuid=uuid, father_name=father_name), re.S)
        # 在父级目录下插入子目录名,例如：4E8A9A502395FDC50067317C /* 单例 */,
        dir_uuid = self.uuid_generator()
        father_sub_str = BASE_PBXGroup_SECTION_ALONE.format(ref_uuid=dir_uuid, file_name=name)
        # print('father_sub_str:', father_sub_str)
        self.write_source(BASE_PBXGroup_SECTION_DIR_PATTERN, father_sub_str)

        # 实现子目录的PBXGroup部分
        # 判断是否是中文,如果是中文，path = ""
        dir_name_ = f'''"{name}"''' if check_chinese(name) else name
        BASE_PBXGroup_SECTION_DIR_STR = BASE_PBXGroup_SECTION_DIR.format(dir_uuid=dir_uuid, dir_name=name,
                                                                         dir_name_=dir_name_)
        self.insert_str_to_project(BASE_PBXGroup_SECTION_DIR_STR, BASE_PBXGroup_SECTION_PATTERN)
        for file_ in file_names:
            # 是文件还是文件夹
            if os.path.isfile(os.path.join(dir_path, file_)):
                file_list.append(file_)
            else:
                dir_list.append(file_)
                self.create_dir(os.path.join(dir_path, file_))

        self.create_files(dir_path, file_list)

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
