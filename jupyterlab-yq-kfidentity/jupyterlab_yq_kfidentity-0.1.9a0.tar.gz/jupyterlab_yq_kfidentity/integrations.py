import requests
import xmltodict
import json
import jwt as pyjwt
import os

from jupyter_server.base.handlers import APIHandler
from tornado.log import app_log
from jupyter_server.utils import url_path_join
from datetime import datetime


JWT_PATH = 'jwt.txt'

def get_jwt():
    try:
        with open(JWT_PATH, 'r') as jwt:
            return jwt.read()
    except:
        app_log.error('Failed to read a JWT.')
        return None
    
def has_expired(token, alg='HS512'):
    decoded = pyjwt.decode(token, options={"verify_signature": False}, algorithms=alg)
    jwt_expired_date = datetime.fromtimestamp(int(decoded['exp']))
    now = datetime.now()
    return jwt_expired_date < now
        

class YqKfIdentity(APIHandler):
    def get(self):
        headers = self.request.headers
        jwt = get_jwt()
        
        if jwt is None or has_expired(jwt, alg='RS256'):
            if "userid-token" in headers:
                with open(JWT_PATH, 'w') as out:
                    out.write(headers["userid-token"])
            else:
                app_log.warn('There is no JWT token in the headers')
                self.set_status(500)
            self.finish(f"JWT Found: {headers['userid-token']}")
        else:
            self.finish('Kubeflow JWT is valid and not expired.')


class YqMinioIntegration(APIHandler):
    def get(self):
        jwt = get_jwt()
        if jwt is not None:
            # Check if AWS Session Token is there and not expired
            if 'AWS_SESSION_TOKEN' in os.environ and not has_expired(os.environ['AWS_SESSION_TOKEN']):
                self.finish('Minio credentials are still valid.')
            else: 
                params = (
                    ('Action', 'AssumeRoleWithWebIdentity'),
                    ('DurationSeconds', '3600'),
                    ('Version', '2011-06-15'),
                    ('WebIdentityToken', jwt),
                )

                response = requests.post('http://yq-storage-viewer.yq:9000/', params=params)
                if response.status_code == 200:
                    minio_response = json.dumps(xmltodict.parse(response.content))
                    app_log.info(minio_response)
                    credentials = minio_response['AssumeRoleWithWebIdentityResponse']['AssumeRoleWithWebIdentityResult']['Credentials']
                    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
                    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
                    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']
                    self.finish(f"Minio credentials: {credentials}")
                else:
                    app_log.error(f'Failed to create STS credentials in Minio: {response.content}')
    

def setup_handlers(web_app):
    """
    Setups all of the YQ ID integrations.
    Every handler is defined here to be integrated with JWT.
    """
    host_pattern = ".*"

    # add the baseurl to our paths
    base_url = web_app.settings["base_url"]
    handlers = [
        (url_path_join(base_url, "yqid", "sync"), YqKfIdentity),
        (url_path_join(base_url, "yqid", "minio"), YqMinioIntegration),
    ]

    
    web_app.add_handlers(host_pattern, handlers)