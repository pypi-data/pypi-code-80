#!/usr/bin/env python
# -*- coding:utf-8
import requests
from . import data

username=""
password=""

#----baidu文字识别配置
'''words默认主目录设置'''
_words_path = "E:\\pool\\"

#----baidu图像识别配置
'''image默认主目录设置'''
_image_path = "E:\\pool\\"

#----baidu语音识别配置
'''speech默认主目录设置'''
_speech_path = "E:\\pool\\"

#----files文件操作配置
'''files默认主目录设置'''
_files_path = "E:\\pool\\"

#----API 鉴权
def AccessToken(_Com,_Class,_API_Key, _Secret_Key):
    def Run(_Com,_Class):
        '''请勿手动修改redis的access_token数据，否则有可能导致程序失效'''
        if data.Get( str( _Com ) + '_' + str( _Class ) + '_access_token' ):
            data.Close()
            return 0
        else:
            _host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + _API_Key + '&client_secret=' + _Secret_Key
            response = requests.get( _host )
            if response:
                _value = response.json()['access_token']
                data.Set( str( _Com ) + '_' + str( _Class ) + '_access_token', _value, ex=3600 * 24 * 29 )
                data.Close()
                return 1

    '''
    _Com参数：
        0 代表百度API

    _Class参数:
        0 代表文字识别access_token
        1 代表图像识别access_token
        2 代表EasyDL定制化模型access_token
        3 代表语音识别

    返回值：
        1 代表access_token生成成功
        0 代表access_token生成失败
    '''
    if _Com==0 and _Class == 0:
        return Run( _Com, _Class )
    if _Com==0 and _Class == 1:
        return Run( _Com, _Class )
    if _Com==0 and _Class == 2:
        return Run( _Com, _Class )
    if _Com==0 and _Class == 3:
        return Run( _Com, _Class )