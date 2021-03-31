import requests
import json
import traceback
from microservice_template_core.tools.logger import get_logger
import urllib3

logger = get_logger()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IcingaCollector(object):
    def __init__(self, ms_source, event_id):
        self.ms_source = ms_source
        self.alerts_count = 0
        self.event_id = event_id
        self.headers = {
            'Accept': 'application/json',
            'X-HTTP-Method-Override': 'GET'
        }

    @staticmethod
    def ms_notification_output(result_body):
        output = {
            "NOTIFICATIONAUTHORNAME": "",
            "SERVICENOTES": "",
            "SERVICENAME": result_body['attrs']['name'],
            "SERVICEDOWNTIME": "0",
            "SERVICEACTIONURL": "",
            "HOSTNAME": result_body['joins']['host']['name'],
            "HOSTADDRESS": result_body['joins']['host']['address'],
            "SEVERITY": result_body['attrs']['severity'],
            "SERVICENOTESURL": "",
            "LASTSTATETYPE": result_body['attrs']['state_type'],
            "NOTIFICATIONTYPE": "PROBLEM",
            "HOSTSERVICE": "",
            "HOSTROLE": "",
            "ICINGASERVER": "",
            "SERVICESTATE": result_body['attrs']['state'],
            "SERVICEOUTPUT": result_body['attrs']['last_check_result']['output'],
            "SERVICESTATETYPE": "",
            "NOTIFICATIONCOMMENT": "",
            # "PROCEDURE_ID": "2387",
            "PROBLEMTYPE": result_body['type'],
            "SERVICEGRAPH": ""
        }

        return output

    @staticmethod
    def ms_unique_name(result_body):
        unique_name = f"other:::{result_body['joins']['host']['name']}:::{result_body['attrs']['name']}"

        return unique_name

    def collect_services(self):
        alerts_per_host = {}

        request_url = "{0}:5665/v1/objects/services".format(self.ms_source['url'])
        data = {
            "joins": ["host.name", "host.address"],
            "filter": "service.state != 0"
        }

        response = requests.post(
            request_url,
            headers=self.headers,
            auth=(self.ms_source['user'], self.ms_source['password']),
            verify=False,
            data=json.dumps(data),
            timeout=5
        ).json()

        for result in response['results']:
            notification_body = self.ms_notification_output(result_body=result)
            ms_unique_name = self.ms_unique_name(result_body=result)
            alerts_per_host[ms_unique_name] = notification_body

            self.alerts_count += 1

        logger.info(
            msg=f"Collected list of alerts from Icinga:\n{alerts_per_host}",
            extra={'tags': {'event_id': str(self.event_id)}}
        )

        return alerts_per_host

    def collect_alerts(self):
        alerts_per_host = self.collect_services()

        request_url = "{0}:5665/v1/objects/hosts".format(self.ms_source['url'])
        data = {
            "attrs": ["last_state"],
            "filter": "host.last_state != 0"
        }

        response = requests.post(
            request_url,
            headers=self.headers,
            auth=(self.ms_source['user'], self.ms_source['password']),
            verify=False,
            data=json.dumps(data),
            timeout=5
        ).json()

        if len(response['results']) == 0:
            return alerts_per_host, self.alerts_count

        for result in response['results']:
            notification_body = self.ms_notification_output(result_body=result)
            ms_unique_name = self.ms_unique_name(result_body=result)
            alerts_per_host[ms_unique_name] = notification_body

            self.alerts_count += 1

        return alerts_per_host, self.alerts_count

    def main(self):
        return self.collect_alerts()

