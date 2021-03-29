import os
import requests
import json
from datetime import datetime, date

# The absolute path of the directoy for this file:
_ROOT = os.path.abspath(os.path.dirname(__file__))

def default(o):
    if isinstance(o, (date, datetime)):
        # return o.isoformat()
        return o.strftime("%Y-%m-%dT%H:%M:%S.000+00:00")

class CVStudio(object):
    def __init__(self, token=None, base_url=None):
        if token == None:
            self.token = os.environ.get('CV_STUDIO_TOKEN')
        else:
            self.token = token

        if self.token == None:
            raise Exception('need to pass valid token or set CV_STUDIO_TOKEN environment variable')

        if base_url == None:
            self.base_url = os.environ.get('CV_STUDIO_BASE_URL', 'https://vision.skills.network')
        else:
            self.base_url = base_url

    def report(self, started=None, completed=None, url=None, parameters=None, accuracy=None, model=None):
        data = {}

        if started is not None:
            data['started'] = started
        
        if completed is not None:
            data['completed'] = completed

        if parameters is not None:
            data['parameters'] = parameters

        if accuracy is not None:
            data['accuracy'] = accuracy

        if model is not None:
            data['model'] = model

        if url is not None:
            data['url'] = url
        
        if len(data) == 0:
            raise Exception('Nothing to report')

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        
        x = requests.post(self.base_url + '/api/report', headers=headers, data=json.dumps(data, default=default))

        return x
