# 기본 내장 모듈
import hashlib
import base64
import random
import sys, os
import shutil

# pip install 패키지
import paramiko

class Mqtt:

    def __init__(self):
        self.protocolDict = dict()
        self.protocolDict["sftp"] = SFTP

    def set_filemanager(self, configDict, protocol=None):
        if protocol is None:
            protocol = "sftp"
        self.filemanager = self.protocolDict[protocol](configDict)

    def register_client(self, configDict, serverPath, filename, clientDict, protocol=None):
        self.set_filemanager(configDict, protocol)
        self.download_passwd_file(serverPath, filename)
        for clientname in clientDict:
            self.check_client(clientname)
        self.passwdFile += "\n"
        print(self.passwdFile)
        print()
        for clientname, passwd in clientDict.items():
            self.add_client(clientname, passwd)
        print()
        self.edit_passwd_file()
        self.upload_passwd_file(serverPath, filename)
        if os.path.isfile(os.path.join(self.filemanager.localPath, filename)):
            os.remove(os.path.join(self.filemanager.localPath, filename))
            print(filename + " 업로드 후 삭제 완료")


    def generate_passwd(self, passwd):
        passwd = passwd.encode()
        chars   = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        salt    = bytes([random.choice(chars) for i in range(16)])
        saltB64 = base64.b64decode(salt)

        m = hashlib.sha512()
        m.update(passwd)
        m.update(saltB64)
        dg = m.digest()

        result = '$6$%s$%s' % (repr(salt)[2:-1],repr(base64.b64encode(dg))[2:-1])
        return result

    def check_client(self, clientId):
        clientList = self.passwdFile.split('\n')
        resultList = list()
        result = str()

        for client in clientList:
            check = client.split(':')
            
            if check[0] != clientId:
                resultList.append(client)
            else:
                print(check[0] + " is detected")
        for client in resultList:
            if client != '':
                result += client + '\n'
        self.passwdFile = result

    def add_client(self, clientId, passwd):
        # can be used after self.check_client
        passwd = self.generate_passwd(passwd)
        self.passwdFile = self.passwdFile + clientId + ":" + passwd + '\n'
        print(clientId + " is added")
    
    def edit_passwd_file(self):
        if os.path.isfile(self.passwdFilePath):
            os.remove(self.passwdFilePath)
        else:
            print("edit_passwd_file error: passwd_file not exist")
        f = open(self.passwdFilePath, 'w+')
        f.write(self.passwdFile)
        f.close()
        print("MQTT 클라이언트 변경사항 적용 완료\n")

    def download_passwd_file(self, serverPath, filename):
        self.filemanager.download(serverPath, filename)
        self.read_passwd_file(filename)

    def read_passwd_file(self, filename, path=None):
        if path == None:
            path = os.path.dirname(sys.argv[0])
        self.passwdFilePath = os.path.join(path, filename)
        try:
            f = open(self.passwdFilePath)
        except:
            print("download_passwd_file error: Cannot open password file")
            os.system("Pause")
            exit()

        self.passwdFile = f.read()
        f.close()

    def upload_passwd_file(self, serverPath, filename):
        try:
            self.filemanager.upload(serverPath, filename)
        except:
            print("예외 발생")
            os.system("Pause")
            exit()

class SFTP:
    def __init__(self, configDict):
        self.host = configDict['host']
        self.port = int(configDict['port'])
        self.username = configDict['username']
        self.passwd = configDict['passwd']
        self.localPath = os.path.dirname(sys.argv[0])
        self.connected = False
    
    def connect(self):
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.connected = True
        except Exception:
            print("SFTP 서버나 포트 확인 바랍니다")
            os.system("Pause")
            exit()

        try:
            self.transport.connect(username = self.username, password = self.passwd)
        except:
            print("아이디나 비밀번호 확인 바랍니다")
            os.system("Pause")
            exit()

        self.client = paramiko.SFTPClient.from_transport(self.transport)
    
    def disconnect(self):
        if self.connected == True:
            try:
                self.client.close()
                self.transport.close()
                self.connected = False
            except:
                print("SFTP disconnect() is Failed")
        else:
            print("SFTP is already not connected")

    def download(self, serverPath, filename, localPath=None):
        if localPath != None:
            self.localPath = localPath
        else:
            localPath = self.localPath
        if self.connected == False:
            self.connect()
        
        serverFilePath = serverPath + '/' + filename
        localFilePath = os.path.join(localPath, filename)

        if os.path.isfile(localFilePath):
            os.remove(localFilePath)
            print("기존 " + filename + " 파일 제거\n")
        try:
            self.client.get(serverFilePath, localFilePath)
            print("다운로드 완료")
            print(localFilePath)
            print()
        except:
            print("다운로드 실패. 파일명은 확장자명까지 포함되어야합니다")
            print("sftp: " + self.host + ":" + str(self.port) + " " + serverFilePath + "\n")
            os.remove(localFilePath)

        self.disconnect()
        return localFilePath

    def upload(self, serverPath, filename, localPath=None):
        if localPath != None:
            self.localPath = localPath
        else:
            localPath = self.localPath
        if self.connected == False:
            self.connect()
        
        serverFilePath = serverPath + '/' + filename
        localFilePath = os.path.join(localPath, filename)

        if os.path.isfile(localFilePath) == False:
            print(localFilePath + "이 존재하지 않습니다")
        try:
            self.client.put(localFilePath, serverFilePath)
            print("업로드 완료")
            print(serverFilePath)
            print()
        except:
            print("업로드 실패")
            print("sftp: " + self.host + ":" + str(self.port) + " " + serverFilePath + '\n')
        self.disconnect()