import os
import sys

sys.path.append(os.path.dirname(__file__) + os.sep + './')

from dataset.dataset import Dataset
from dataset.file import File
from dataset.localdb import LocalDb

#sdk入口
class TDA():
    def __init__(self, access_key, secret_key, endpoint="http://127.0.0.1:8888/", type="minio"):
        #todo::后续此处应变为远程查询 ak sk
        self.dataset = Dataset(access_key, secret_key, endpoint, type)
        self.commitFlag = False
        self.commitId = ""
        self.datasetName = ""
        self.fileList = []

    def SetDataset(self, datasetName):
        self.datasetName = datasetName

    def RiseException(self):
        raise Exception("You have not set the dataset name yet!")

    def ListAllDataset(self, recu=False):
        if not self.datasetName:
            self.RiseException()

        return self.dataset.ListAllDataset(self.datasetName, recu)

    def CreateDataset(self, datasetName):
        return self.dataset.CreateDataset(datasetName)

    def UploadFilesToDataset(self, rootPath, ext="", batchNum=0):
        if not self.datasetName:
            self.RiseException()

        return self.dataset.PutFilesToDataset(self.datasetName, rootPath, ext, batchNum)

    def UploadFileToDataset(self, objectName, filePath):
        if not self.datasetName:
            self.RiseException()
        return self.dataset.PutFileToDataset(self.datasetName, objectName, filePath)

    def DeleteFileFromDataset(self, objectName):
        if not self.datasetName:
            self.RiseException()

        return self.dataset.DeleteFromDataset(self.datasetName, objectName)

    def AddFile(self, filepath, basepath=""):
        if not self.datasetName:
            self.RiseException()

        file = File(filepath, basepath)
        self.fileList.append(file)
        return file


    def Commit(self, commitId = ""):
        if not self.datasetName:
            self.RiseException()

        db = LocalDb(commitId)
        db.insertVal(self.fileList)
        db.close()

        self.commitFlag = True
        self.commitId = db.commitId
        return db.commitId


    def Upload(self, commitId = ""):
        if not self.datasetName:
            self.RiseException()

        if commitId != "":
            self.commitFlag = True
            self.commitId = commitId

        if not self.commitFlag:
            self.commitId = self.Commit(commitId)

        if not self.commitId:
            self.commitId = self.Commit(commitId)

        db = LocalDb(commitId)
        allData = db.fetchAll()

        for row in allData:
            self.UploadFileToDataset(row[2], row[0])


        #todo:批量同步数据，一千个结果同步一次

        db.close()








