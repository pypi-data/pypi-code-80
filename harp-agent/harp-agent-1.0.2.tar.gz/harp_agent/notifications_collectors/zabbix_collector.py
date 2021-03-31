import requests
import json
import traceback
import harp_agent.settings as settings
from microservice_template_core.tools.logger import get_logger
import urllib3

logger = get_logger()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ZabbixCollector(object):
    def __init__(self, ms_source, event_id):
        self.ms_source = ms_source
        self.alerts_count = 0
        self.event_id = event_id
        self.headers = {
            'Content-Type': 'application/json-rpc'
        }

    def ms_notification_output(self, result_body):
        output = {
            'host.name': result_body['hosts'][0]['name'],
            'item.value1': result_body['value'],
            'item.key1': '',  # Don`t present
            'trigger.severity': result_body['priority'],
            'trigger.name': result_body['description'],
            'trigger.expression': result_body['expression'],
            'source': self.ms_source['url'],
            'trigger.description': '',  # Don`t present
            'item.id1': result_body['items'][0]['itemid'],
            'trigger.url': result_body['url'],
            'triggerid': result_body['triggerid'],
            'trigger.hostgroup.name': '',  # Don`t present
            'trigger.status': 'PROBLEM'
        }

        return output

    @staticmethod
    def ms_unique_name(result_body):
        unique_name = f"other:::{result_body['hosts'][0]['name']}:::{result_body['description']}"

        return unique_name

    def zabbix_auth(self):
        auth_json = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.ms_source['user'],
                "password": self.ms_source['password']
            },
            "id": 1,
            "auth": None
        }

        auth = requests.post(
            url=f"{self.ms_source['url']}/api_jsonrpc.php",
            headers=self.headers,
            data=json.dumps(auth_json),
            timeout=5
        ).json()

        if 'result' in auth:
            auth = auth['result']

        logger.info(
            msg=f"Successfully logged into Zabbix: {auth}",
            extra={'tags': {'event_id': str(self.event_id)}}
        )

        return auth

    def collect_triggers(self):
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": ['description', 'priority', 'value', 'expression', 'url'],
                "filter": {
                    "value": 1,
                    "status": 0
                },
                "state": 0,
                "active": True,
                "withLastEventUnacknowledged": True,
                "expandDescription": 1,
                "expandExpression": 1,
                "expandComment": 1,
                "selectHosts": ["name"],
                "selectItems": ["item"],
                "selectGroups": ["group"]
            },
            "auth": self.zabbix_auth(),
            "id": 1
        }

        result = requests.post(
            url=f"{self.ms_source['url']}/api_jsonrpc.php",
            headers=self.headers,
            data=json.dumps(data)
        ).json()

        logger.info(
            msg=f"Collected triggers from Zabbix:\n{result}",
            extra={'tags': {'event_id': str(self.event_id)}}
        )

        return result

    def process_result(self):
        alerts_per_host = {}
        result = self.collect_triggers()

        if 'result' in result:
            for trigger in result['result']:
                notification_body = self.ms_notification_output(result_body=trigger)
                ms_unique_name = self.ms_unique_name(result_body=trigger)
                alerts_per_host[ms_unique_name] = notification_body
                self.alerts_count += 1

        return alerts_per_host, self.alerts_count

    def main(self):
        return self.process_result()



