# coding = utf-8
import requests, re, os
from math import *
def download(data_src):
    headers = {"User-Agent": "Microsoft Edge/89.0.774.57 Windows"}
    flag = 0
    if not os.path.isdir('./firmwares'):
        os.mkdir('./Firmwares')
        flag = 1
    counter = 0
    for data in data_src:
        print('\nGetting information in the url......')
        response = requests.get(url=data, headers=headers)
        print('Start downloading ' + data + ' , count = %d, size = %d KB'
              % (counter + 1, round(float(response.headers['Content-Length']) / 1024, 2)))
        File_Name = './Firmwares/' + re.sub("',\\)", '', re.split('/', str(data))[-1])
        if (flag == 0 and os.path.isfile(File_Name)):
            continue
        fp = open(File_Name, 'wb')
        fp.write(response.content)
        print(data + ' downloaded.')
        counter += 1
    print('Finished.')
