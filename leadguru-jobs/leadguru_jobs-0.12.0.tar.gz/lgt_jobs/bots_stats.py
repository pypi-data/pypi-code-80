import time
from abc import ABC
from typing import Optional

import yaml
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.model import BotModel
from lgt_data.mongo_repository import BotMongoRepository
from pydantic import BaseModel
from lgt.common.python.lgt_logging import log

from .env import k8config_path, k8namespace, backend_uri, aggregator_topic, project_id, \
    google_app_credentials
from . import BaseBackgroundJobData, BaseBackgroundJob

"""
Update bots statistics
"""
class BotStatsUpdateJobData(BaseBackgroundJobData, BaseModel):
    bot_name: str

class BotStatsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotStatsUpdateJobData

    def exec(self, data: BotStatsUpdateJobData):
        bots_rep = BotMongoRepository()
        bot = bots_rep.get_by_id(data.bot_name)

        client = SlackWebClient(bot.token, bot.cookies)
        channels = client.channels_list()['channels']
        bot.connected_channels = sum(1 for channel in channels if channel['is_member'])
        bot.channels = len(channels)
        bots_rep.add_or_update(bot)


"""
Bots Credentials update
"""
class BotsCredentialsUpdateData(BaseBackgroundJobData, BaseModel):
    bot_name: str


class BotsCredentialsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotsCredentialsUpdateData

    def exec(self, data: BotsCredentialsUpdateData):
        bots_rep = BotMongoRepository()
        bot = bots_rep.get_by_id(data.bot_name)

        creds = SlackWebClient.get_access_token(bot.slack_url, bot.user_name, bot.password)
        if not creds:
            print(f'{bot.name}....[INVALID_CREDS]')
            bot.invalid_creds = True
            bots_rep.add_or_update(bot)
            return

        bot.token = creds.token
        bot.cookies = creds.cookies
        bot.invalid_creds = False
        bots_rep.add_or_update(bot)
        print(f'{bot.name}....[UPDATED]')


"""
Restart Bots
"""
class RestartBotsJobData(BaseBackgroundJobData, BaseModel):
    bots: [str]
    chunk_size: Optional[int] = 30

class RestartBotsJob(BaseBackgroundJob, ABC):
    def _remove_bots(self):
        from .k8client import KubernetesClientFactory

        k8client = KubernetesClientFactory.create(k8config_path)
        deployments_list = k8client.list_namespaced_deployment(namespace=f'{k8namespace}')

        for dep in deployments_list.items:
            if dep.metadata.labels and dep.metadata.labels.get('type', '') == 'slack-bot':
                k8client.delete_namespaced_deployment(dep.metadata.name, dep.metadata.namespace)

        time.sleep(15)

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _update_bots(self, name, bots: [BotModel]):
        from kubernetes.client import ApiException
        from .k8client import KubernetesClientFactory

        k8client = KubernetesClientFactory.create(k8config_path)
        with open("templates/bots_service_template.yaml") as f:
            template = yaml.safe_load(f)
            containers = list()

            for bot in bots:
                if 'token' not in bot:
                    continue

                container = {
                    'name': bot['name'],
                    'image': 'gcr.io/lead-tool-generator/lgt-slack-aggregator:latest',
                    'volumeMounts': [{
                        'name': 'google-cloud-key',
                        'mountPath': '/var/secrets/google'
                    }],
                    'imagePullPolicy': 'Always',
                    'resources': {
                        'requests': {
                            'memory': '32Mi',
                            'cpu': '10m'
                        },
                        'limits': {
                            'memory': '48Mi',
                            'cpu': '10m'
                        }
                    },
                    'env': [
                        {'name': 'PUBSUB_PROJECT_ID', 'value': project_id},
                        {'name': 'PUBSUB_TOPIC_OUT', 'value': aggregator_topic},
                        {'name': 'SLACKBOT_TOKEN', 'value': bot.token},
                        {'name': 'SLACKBOT_NAME', 'value': bot.name},
                        {'name': 'COUNTRY', 'value': bot.country},
                        {'name': 'REGISTRATION_LINK', 'value': bot.registration_link },
                        {'name': 'GOOGLE_APPLICATION_CREDENTIALS', 'value': google_app_credentials},
                        {'name': 'BACKEND_URI', 'value': backend_uri}
                    ]
                }
                containers.append(container)

            template['spec']['template']['spec']['containers'] = containers
            template['metadata']['name'] = name
            template['spec']['selector']['matchLabels']['app'] = name
            template['spec']['template']['metadata']['labels']['app'] = name

            exists = True
            try:
                k8client.read_namespaced_deployment(name, k8namespace)
            except ApiException as e:
                if e.status == 404:
                    exists = False

            if exists:
                print(f'{name} deleting the old deployment')
                k8client.delete_namespaced_deployment(name, namespace=f'{k8namespace}')
                time.sleep(20)

            print(f'{name} creating new deployment')
            result = k8client.create_namespaced_deployment(namespace=f'{k8namespace}', body=template)

            return result

    @property
    def job_data_type(self) -> type:
        return RestartBotsJobData

    def exec(self, data: RestartBotsJobData):
        self._remove_bots()
        repo = BotMongoRepository()
        bots = repo.get()

        chunk_list = self._chunks(list(filter(lambda x: not x.get("invalid_creds", False), bots)), data.chunk_size)
        index = 0

        from kubernetes.client import V1Deployment
        for chunk in chunk_list:
            name = f'lgt-bots-{index}'
            response: V1Deployment = self._update_bots(name, list(chunk))
            log.info(f'Deployment {index} has been updated.')
            index = index + 1

