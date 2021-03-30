# -*- coding: utf-8 -*-
# @Time : 2021/3/5
# @Author : NotOne
# @Email : lvsongke@tianyancha.com
import json
import datetime
import time
import hashlib


def saveErrorMessage(path, message):
    if not message:
        return
    with open(path, 'a') as fs:
        if not isinstance(message, str):
            fs.write(json.dumps(message) + '\n')
        else:
            fs.write(message + '\n')


def getTime(format='%Y%m%d', days=None, hour=None, seconds=None, minute=None, timeType=None):
    if days == 'now':
        date = datetime.datetime.now()
    elif not days is None and isinstance(days, int):
        today = datetime.datetime.today()
        date = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
        date = date + datetime.timedelta(days=days)
    elif not hour is None and isinstance(hour, int):
        today = datetime.datetime.today()
        date = datetime.datetime(today.year, today.month, today.day, today.hour, 0, 0)
        date = date + datetime.timedelta(hours=hour)
    elif not seconds is None and isinstance(seconds, int):
        today = datetime.datetime.today()
        date = datetime.datetime(today.year, today.month, today.day, today.hour, today.minute, today.second)
        date = date + datetime.timedelta(seconds=seconds)
    elif not minute is None and isinstance(minute, int):
        today = datetime.datetime.today()
        date = datetime.datetime(today.year, today.month, today.day, today.hour, today.minute, today.second)
        date = date + datetime.timedelta(minutes=minute)
    else:
        raise ValueError('参数错误')

    if timeType == 'ts':
        return int(time.mktime(date.timetuple()))
    return date.strftime(format)


def parseSetCookie(cookieStr, cookieType='string'):
    cookieList = cookieStr.split(',')
    cookieDict = {}
    res = cookieDict
    for cookies in cookieList:
        if '=' in cookies:
            formatCookie = cookies.split(';')[0]
            kv = formatCookie.split('=', maxsplit=1)
            if len(kv) > 1:
                k, v = kv[0].strip(), kv[1].strip()
                cookieDict[k] = v
    if cookieDict and cookieType == 'string':
        res = ';'.join(['='.join(kv) for kv in cookieDict.items()])
    return res


def getMd5(content):
    md5 = hashlib.md5()
    md5.update(content.encode())
    return md5.hexdigest()


def getNowTimeStr():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def dateFormat(dateString, format):
    if not dateString or dateString == '0000/00/00':
        return None
    return datetime.datetime.strptime(dateString, format).__str__()


if __name__ == '__main__':
    res = getTime(days=2, timeType='ts')
    print(getNowTimeStr())
