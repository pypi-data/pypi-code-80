from . import api_base
from . import utils
try:
    from StringIO import StringIO
except:
    from io import StringIO
import hashlib,json,os,pdb

from ...config.default_config import *


def login(username=None, password=None):
    http_client = api_base.__get_conn__()
    request_string = []
    request_string.append('auth/oauth/login')
    body = {'username':username, 
            'password': hashlib.md5(password.encode('utf8')).hexdigest()}
    result = api_base.__get_result__(method='POST',request_string=''.join(request_string), 
                                     body=body, http_client=http_client, gw=True, auth=False)
    
    jtw = json.loads(result)
    if 'user' in jtw:
        os.environ.setdefault('seleya_id', str(jtw['user']['uid']))
        print("""UID({0}) Login Success""".format(str(jtw['user']['uid'])))
    if 'clients' in jtw:
        os.environ.setdefault('seleya_client_id', jtw['clients'][0]['client_id'])
        os.environ.setdefault('seleya_client_secret', jtw['clients'][0]['client_secret'])
    
    '''
    body={'grant_type':'password','username':username,
          'password':hashlib.md5(password.encode('utf8')).hexdigest(),'scope':'profile'},
    request_string = []
    request_string.append('auth/oauth/token')
    api_base.__get_result__(method='POST',request_string=''.join(request_string), 
                                     body=body, http_client=http_client, gw=True, auth=True)
    '''