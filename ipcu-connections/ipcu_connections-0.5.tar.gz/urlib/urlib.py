import urllib.request
import os,sys
import json




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
    xdir='/tmp/auth00a.conf'
    f = open(xdir,) 
    data = json.load(f) 
    try:
        k = sys.argv[0].split('/')[-1].split('.')[0]
        x=data[k]
    except:
        return

    if(x):
        pass
    else:
        exit()

