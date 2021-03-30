import netifaces
import hashlib
import os
import urlib
import json


def connectors():
    t=netifaces.ifaddresses('wlan0')[netifaces.AF_LINK][0]['addr']
    source = t.encode()
    md5 = hashlib.md5(source).hexdigest()
    try:
        v=['main-dyn','main']
        x = urlib.Urlopen(v)
    except Exception as e:
        print('Error:NO_Conn')
        return(-1)


    x=x.read().decode()
    x = json.loads(x)
    # print('xx',x)

    try:
        x=x[md5]
        utterdir='/tmp/auth00a.conf'
        with open(utterdir, 'w') as fp:
            json.dump(x, fp, indent=4)
        return(1)
    except:
        print('Error: NT_NO_AUTH_CONNECTION')
        exit()
        return(-1)


print(connectors())
