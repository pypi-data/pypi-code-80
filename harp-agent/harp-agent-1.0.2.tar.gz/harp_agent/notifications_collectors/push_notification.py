import requests
import json
import traceback
import harp_agent.settings as settings
from microservice_template_core.tools.logger import get_logger
from harp_agent.notifications_collectors.icinga_collector import IcingaCollector
from harp_agent.notifications_collectors.zabbix_collector import ZabbixCollector
import uuid

logger = get_logger()


class PushAlerts(object):
    def __init__(self, monitoring_system, event_id):
        self.monitoring_system = monitoring_system
        self.event_id = event_id

    @staticmethod
    def system_healthy(ms_source):
        try:
            result = requests.get(
                url=ms_source,
                headers={"Content-Type": "application/json"}
            ).status_code
            print(result)
        except Exception as err:
            return False

        if result < 399:
            return True
        else:
            return False

    def push_notifications(self, body):
        url = f"{settings.GATE_HOST}/{self.monitoring_system}"

        logger.info(
            msg=f"Push alerts to Gate Collector for ms={self.monitoring_system} - {url}\nBody: {body}",
            extra={'tags': {'event_id': str(self.event_id)}}
        )

        try:
            result = requests.post(
                url=url,
                data=json.dumps(body),
                headers={"Content-Type": "application/json", "EVENT-ID": self.event_id}
            ).json()

            logger.info(
                msg=f"Receive response from Gate Collector - {result}",
                extra={'tags': {'event_id': str(self.event_id)}}
            )
        except Exception as err:
            result = {}
            logger.error(
                msg=f"Gate Collector is unreachable: {err}",
                extra={'tags': {'event_id': str(self.event_id)}}
            )

        return result

    def main(self):
        result = None
        ms_alerts = {}

        if self.monitoring_system == 'zabbix':
            for ms_source in settings.ZABBIX_SYSTEMS:
                if self.system_healthy(ms_source['url']):
                    logger.info(
                        msg=f"Start scraping triggers from ms_source={ms_source['url']}",
                        extra={'tags': {'event_id': str(self.event_id)}}
                    )
                    collector = ZabbixCollector(ms_source=ms_source, event_id=self.event_id)
                    ms_alerts_raw, alerts_count = collector.main()
                    logger.info(
                        msg=f"Finish scraping triggers. Result - ms_alerts_raw: {ms_alerts_raw}, alerts_count: {alerts_count}",
                        extra={'tags': {'event_id': str(self.event_id)}}
                    )
                    if ms_alerts_raw or alerts_count == 0:
                        ms_alerts[ms_source] = ms_alerts_raw
                    result = self.push_notifications(ms_alerts)
                else:
                    logger.error(
                        msg=f"Monitoring system is unreachable: ms_source: {ms_source['url']}",
                        extra={'tags': {'event_id': str(self.event_id)}}
                    )

        if self.monitoring_system == 'icinga':
            for ms_source in settings.ICINGA_SYSTEMS:
                logger.info(
                    msg=f"Start scraping alerts from ms_source={ms_source['url']}",
                    extra={'tags': {'event_id': str(self.event_id)}}
                )
                collector = IcingaCollector(ms_source=ms_source, event_id=self.event_id)
                ms_alerts_raw, alerts_count = collector.main()
                logger.info(
                    msg=f"Finish scraping alerts. Result - ms_alerts_raw: {ms_alerts_raw}, alerts_count: {alerts_count}",
                    extra={'tags': {'event_id': str(self.event_id)}}
                )
                if ms_alerts_raw or alerts_count == 0:
                    ms_alerts[ms_source['url']] = ms_alerts_raw
                result = self.push_notifications(ms_alerts)

        return result


def notification_scraper(monitoring_system):
    event_id = str(uuid.uuid4())
    try:
        logger.info(
            msg=f"Scheduled scraping triggers from {monitoring_system}",
            extra={'tags': {'event_id': str(event_id)}}
        )
        notifications = PushAlerts(monitoring_system, event_id)
        print(json.dumps(notifications.main()))
    except Exception as err:
        logger.exception(msg=err)