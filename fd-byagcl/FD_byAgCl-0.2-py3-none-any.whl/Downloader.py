# coding = utf-8
import requests, re, os
def download(data_src):
    headers = {"User-Agent": "Microsoft Edge/89.0.774.57 Windows"}
    flag = 0
    if not os.path.isdir('./firmwares'):
        os.mkdir('./Firmwares')
        flag = 1
    counter = 0
    for data in data_src:
        if re.findall('^ftp', data[0]):
            continue
        File_Name = './Firmwares/' + re.sub("',\\)", '', re.split('/', str(data))[-1])
        if flag == 0 and os.path.isfile(File_Name):
            continue
        fp = open(File_Name, 'wb')
        print('Start downloading ' + data[0] + ' , count = %d' % (counter + 1))
        fp.write(requests.get(url=data[0], headers=headers).content)
        print(data[0] + ' downloaded.')
        counter += 1
    print('Finished.')
