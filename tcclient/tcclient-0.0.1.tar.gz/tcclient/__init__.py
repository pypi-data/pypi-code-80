__author__ = 'Andrey Komissarov'
__email__ = 'andrey.komissarov@starwind.com'
__date__ = '2020.03'

import time
from dataclasses import dataclass
from urllib.parse import urljoin

import requests

from tcclient.logger import logger


@dataclass
class TCRestClient:
    """Main class to interact with the TeamCity server through REST API

    https://www.jetbrains.com/help/teamcity/rest-api-reference.html
    """

    base_url: str
    token: str

    def __post_init__(self):
        self.header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def get_server_info(self):
        # /app/rest/server

        url = self._create_url('projects')
        logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_all_build_types(self):
        # /app/rest/buildTypes

        url = self._create_url('buildTypes')
        logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_build_types_info(self, uid: str):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :return:
        """

        base = self._create_url('buildTypes')
        url = f'{base}/id:{uid}'
        logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_build_types_steps(self, uid: str):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :return:
        """

        base = self._create_url('buildTypes')
        url = f'{base}/id:{uid}/steps'
        logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def get_all_projects(self):

        url = self._create_url('projects')
        logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_project_info(self, uid: str):
        """

        :param uid: ID
        :return:
        """

        base = self._create_url('projects')
        url = f'{base}/id:{uid}'

        logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def run_build_types(self, uid: str, comment: str = None):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :param comment:
        :return:
        """

        url = self._create_url('buildQueue')

        comment_ = comment if comment is not None else 'API BOT did it...'
        data = {
        	'buildType': {
            	'id': uid
        	},
            'comment': {
                'text': comment_
            }
        }

        logger.info(f'POST | {url}')

        return requests.post(url, headers=self.header, json=data)

    def get_queued_build(self, uid: str):
        # [GET] http://<TeamCity Server host>:<port>/app/rest/buildQueue?locator=<BuildQueueLocator>

        url = self._create_url('buildQueue')
        params = {
            'locator' : uid
        }

        logger.info(f'GET | {url}, {params = }')

        return  requests.get(url, headers=self.header, params=params)

    def get_build_state(self, uid: int):
        # [GET] http://<TeamCity Server host>:<port>/app/rest/buildQueue/XXX

        url = self._create_url(f'buildQueue/id:{uid}')

        logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def wait_for_build_completion(self, uid: int):
        response = self.get_build_state(uid)
        state = response.json()['state']
        status = response.json()['status']

        while state == 'running':
            response = self.get_build_state(uid)
            state = response.json()['state']
            status = response.json()['status']
            time.sleep(5)

        logger.info(f'WAITING | {state = }, {status = }')
        return status == 'SUCCESS'

    def _create_url(self, url: str):
        """Create full URL

        :param url:
        :return:
        """

        base = f'{self.base_url}/app/rest/'
        return urljoin(base=base, url=url)
