import os, sys
import hashlib

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from matedata import MateData
from labeldata import LabelData
from utils import util

class File():
    def __init__(self, filepath, basepath):
        self.matedata = {}
        self.labeldata = LabelData()
        if basepath == "":
            self.osspath = os.path.basename(filepath)
        else:
            basepath = basepath.rstrip("/")
            if filepath.find(basepath) < 0:
                raise Exception(f"basepath must be part of filepath!")
            self.osspath = filepath.split(basepath + "/")[1]

        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.md5 = util.getFileMd5(self.filepath)
        self.filesize = util.getFileSize(self.filepath)
        self.type = util.getFiletype(self.filepath)

        with open(self.filepath, "rb") as bf:
            file_md5 = hashlib.md5(bf.read())
            self.md5 = file_md5.hexdigest()

    def AddMateData(self, madedata):
        self.matedata = MateData(madedata)

    #添加box
    def AddBox(self, box, label="", instance="", attrs={}):
        # 数据格式检查
        if not type(box) is dict:
            raise Exception(f"box must be a dict, {type(box)} gavin")

        keys = list(set(box.keys()))
        keys.sort()
        if keys != ['height', 'width', 'x', 'y']:
            raise Exception(f"box keys must be ['height', 'width', 'x', 'y'], {type(box)} gavin")

        self.labeldata.AddLabels(label=label, instance=instance, attrs=attrs, ltype="box", data=box)
