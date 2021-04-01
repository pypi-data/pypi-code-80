#!/usr/bin/env python
# -*- coding:utf-8
import sys
import os
import requests
import json
import base64
from .. import config,data

IS_PY3 = sys.version_info.major
if IS_PY3 == 3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
elif IS_PY3 == 2:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

class Ai():
    def __init__(self):
        # 主目录
        self._words_path = config._words_path
        self._speech_path = config._speech_path
        self._image_path = config._image_path
        data.Close()

    #----文字识别
    def Ocr(self,image,e="low"):
        e=quote_plus(e)
        img_src= self._words_path+image
        files = {'file': (image, open( img_src, 'rb' ), 'image/bmp', {'Expires': '0'})}
        request_url = "http://api.pystargate.com:8000/ocr?e="+e
        response = requests.post( request_url,files = files)
        result_str = response.text
        return result_str

    #----语音识别
    def SpeechSynthesis(self,say,save_file="SpeechSynthesis.mp3"):
        _say = say
        _save_file = save_file
        data = quote_plus( _say )
        request_url = "http://api.pystargate.com:8000/speech?say=" + str( data )
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.get( request_url, headers=headers )
        result_str = response.content

        with open( self._speech_path + _save_file, 'wb+' ) as of:
            of.write( result_str )
            of.close()

        file = self._speech_path + _save_file
        os.system( file )

    #----图像识别
    def ImageSynthesis(self,image):
        img_src= self._image_path+image
        try:
            files = {'file': (image, open( img_src, 'rb' ), 'image/bmp', {'Expires': '0'})}
        except:
            return "未发现文件"
        request_url = "http://api.pystargate.com:8000/image"
        response = requests.post( request_url,files = files)
        result_str = response.text
        keyword_arr=[]
        for i in range(0,len(json.loads( result_str )['result'])):
            keyword = json.loads( result_str )['result'][i]['keyword']
            keyword_arr.append(keyword)
            i = i + 1
        return keyword_arr
