import requests
import subprocess
import sys
import json

#version = requests.get('http://125.227.53.95:10001/gorder/version').text.strip('\n')
version = requests.get('https://api.haohaninfo.com/api/microcast_1/gopy/gopy.txt').text.strip()
pip_list = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json']).decode()
json_list = json.loads(pip_list)

for i in json_list:
    if(i['name'] == 'haohaninfo' and i['version'] != version):
        print("已有最新版本: " + version)
        print("更新指令: pip install haohaninfo --upgrade")