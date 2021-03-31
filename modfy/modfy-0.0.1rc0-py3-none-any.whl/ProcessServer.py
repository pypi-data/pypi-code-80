import json
import requests
from modfy.config import Config


class ProcessServer:

    def __init__(self, operation, isAsync=False, webhookUrl=''):
        self.operation = operation
        self.isAsync = isAsync
        self.webhookUrl = webhookUrl
        config = Config()
        self.API_URL = config.API_URL

    def process(self, token):
        try:
            jsonOp = json.dumps(self.operation.serverOperationJson)
            url = self.API_URL + \
                ('/process/async' if self.isAsync else '/process')
            response = requests.post(url, data=dict(operation=jsonOp, token=token,
                                     webhook=self.webhookUrl), files=dict(video=self.operation.inputFiles[0]))
            response.raise_for_status()
            if self.isAsync:
                return response.json()
            return response.content
        except requests.exceptions.RequestException as e:
            print('Error making process request', e)
            raise SystemExit(e)
