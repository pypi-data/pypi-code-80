import urllib.request
import os,sys
import json

TMP = 'tmp'
AUTH = 'auth00a'


def Urlopen(x):
    protocol = "https:/"
    d = 'raw.githubusercontent.com'
    new = [protocol,d]
    new.extend(x)
    new.append('main')
    new.append('README.md')
    y=urllib.request.urlopen('/'.join(new))
    return(y)


def init_all():
    temp0 = [TMP,AUTH]
    temp1 = '/'+'/'.join(temp0)
    xdir=temp1+'.conf'
    f = open(xdir,) 
    data = json.load(f) 
    try:
        k = sys.argv[0].split('/')[-1].split('.')[0]
        x=data[k]
    except:
        error_msg = " : A Connection attempt failed because the connected partydid not respond after a period of time, or established connection failedbecause connected host has failed to respnd."
        print('Error',error_msg)
        exit()

    if(x):
        pass
    else:
        error_msg = " : A Connection attempt failed because the connected partydid not respond after a period of time, or established connection failedbecause connected host has failed to respnd."
        print('Error',error_msg)
        exit()

