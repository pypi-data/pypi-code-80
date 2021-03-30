import datetime
import time
from abc import ABC
from typing import Optional

import yaml
from lgt.common.python.slack_client.web_client import SlackWebClient, SlackMessageConvertService
from lgt_data.model import BotModel, SlackHistoryMessageModel, UserLeadModel, UserModel
from lgt_data.mongo_repository import BotMongoRepository, UserLeadMongoRepository, UserMongoRepository, \
    UserBotCredentialsMongoRepository
from pydantic import BaseModel, conlist
from lgt.common.python.lgt_logging import log

from .runner import BackgroundJobRunner
from .env import k8config_path, k8namespace, backend_uri, aggregator_topic, project_id, \
    google_app_credentials, portal_url
from . import BaseBackgroundJobData, BaseBackgroundJob
from .smtp import SendMailJob, SendMailJobData

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
UserBots Credentials update
"""
class UserBotsCredentialsUpdateData(BaseBackgroundJobData, BaseModel):
    bot_name: str
    user_id: str

class UserBotsCredentialsUpdateJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return UserBotsCredentialsUpdateData

    def exec(self, data: UserBotsCredentialsUpdateData):
        bots_rep = UserBotCredentialsMongoRepository()
        bot = list(filter(lambda x: x.bot_name == data.bot_name, bots_rep.get_bot_credentials(data.user_id)))
        if not bot:
            log.error(f"Unable to find bot {data.bot_name} for user: {data.user_id}")
            return

        bot = bot[0]
        if bot.invalid_creds:
            return

        creds = SlackWebClient.get_access_token(bot.slack_url, bot.user_name, bot.password)
        if not creds:
            print(f'{bot.name}....[INVALID_CREDS]')
            bots_rep.set(data.user_id, data.bot_name, invalid_creds=True)
            return

        bots_rep.set(data.user_id, data.bot_name, invalid_creds=False, token=creds.token, cookies=creds.cookies, updated_at=datetime.datetime.utcnow())

"""
Restart Bots
"""
class RestartBotsJobData(BaseBackgroundJobData, BaseModel):
    bots: conlist(str, min_items = 0)
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



"""
Load slack chat history
"""
class LoadChatHistoryJobData(BaseBackgroundJobData, BaseModel):
    user_id: str
    days_ago: Optional[int] = 10

class LoadChatHistoryJob(BaseBackgroundJob, ABC):
    @staticmethod
    def _merge_chat_histories(saved_chat, current_chat):
        for message in current_chat:
            if not any(filter(lambda msg: msg['ts'] == message['ts'], saved_chat)):
                saved_chat.append(message)
        return saved_chat

    def _update_history(self, bots_map: dict, user: UserModel, lead: UserLeadModel) -> Optional[SlackHistoryMessageModel]:
        saved_chat_history = list(map(lambda msg: SlackHistoryMessageModel.to_dic(msg), lead.chat_history)) \
            if isinstance(lead, UserLeadModel) else list()
        creds = bots_map.get(lead.message.name)
        if creds.invalid_creds:
            return None

        slack_client = SlackWebClient(creds.token, creds.cookies)
        history = slack_client.chat_history(lead.message.name)

        if not history['ok']:
            log.error(
                f'Failed to fetch chat history for the lead: {lead.id} | {user.email}. ERROR: {history.get("error", "")}')
            return None

        messages = list(
            map(lambda x: SlackMessageConvertService.from_slack_response(user.email, creds.bot_name, creds.token, x),
                history.get('messages', [])))
        messages = sorted(messages, key=lambda x: x.created_at)
        messages = LoadChatHistoryJob._merge_chat_histories(saved_chat=saved_chat_history, current_chat=messages)
        UserLeadMongoRepository().update_lead(lead.user_id, lead.id, chat_history=messages)

        return messages[-1] if messages else None

    def _notify_about_new_messages(self, user: UserModel, lead: UserLeadModel):
        if not lead:
            return

        with open('templates/new_message_mail_template.html', mode='r') as template_file:
            html = template_file.read()
            html = html.replace("{sender}", lead.message.profile.get_name())
            html = html.replace("{view_message_link}", f'{portal_url}/my-leads')

            message_data = {
                "html": html,
                "subject": 'New message(s) on LEADGURU',
                "recipient": user.email
            }

            BackgroundJobRunner.submit(SendMailJob, SendMailJobData(**message_data))

    @property
    def job_data_type(self) -> type:
        return LoadChatHistoryJobData

    def exec(self, data: LoadChatHistoryJobData):
        user = UserMongoRepository().get(data.user_id)
        today = datetime.datetime.utcnow()
        delta = datetime.timedelta(days=data.days_ago)
        leads = UserLeadMongoRepository().get_leads(user_id=data.user_id, skip=0, limit=100, from_date=today - delta)
        log.info(f"[LoadChatHistoryJob]: processing {len(leads)} for user: {user.email}")

        if not leads:
            return

        user_bots = UserBotCredentialsMongoRepository().get_bot_credentials(user_id=data.user_id)
        bots_map = { bot.name: bot for bot in user_bots }

        last_message = None
        last_message_lead = None
        for lead in leads:
            message = self._update_history(bots_map=bots_map, user=user, lead=lead)

            if not message:
                continue

            if not last_message:
                last_message = message
                last_message_lead = lead

            if message.created_at > last_message.created_at:
                last_message = message
                last_message_lead = lead


        if last_message and last_message.created_at > user.new_message_notified_at:
            self._notify_about_new_messages(user, last_message_lead)
            UserMongoRepository().set(data.user_id, new_message_notified_at=datetime.datetime.utcnow())