import netifaces
import hashlib
import os
import urlib
import json
import socket

def connectors():
    interface0=''
    for i in socket.if_nameindex():
        if(i[1][:2]=='wl'):
            interface0=i[1]

    t=netifaces.ifaddresses(interface0)[netifaces.AF_LINK][0]['addr']
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


    try:
        #temp
        md5 = '2728cd752e92e46b51d291ca890f8111'

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
