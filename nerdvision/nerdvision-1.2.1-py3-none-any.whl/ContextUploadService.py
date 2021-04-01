import logging
from concurrent.futures.thread import ThreadPoolExecutor

import requests

from nerdvision import settings

our_logger = logging.getLogger("nerdvision")


class ContextUploadService(object):
    def __init__(self, client_config):
        self.client_config = client_config
        self.url = settings.get_context_url()
        self.api_key = settings.get_setting("api_key")
        self.version = 2
        self.pool = ThreadPoolExecutor(max_workers=2)

    def send_event(self, event_snapshot, session_id):
        try:
            our_logger.debug("Sending snapshot to %s", self.url)
            query = '?breakpoint_id=' + event_snapshot['breakpoint']['breakpoint_id']
            query += '&workspace_id=' + event_snapshot['breakpoint']['workspace_id']
            if 'log_msg' in event_snapshot and event_snapshot['log_msg'] is not None:
                query += '&log_msg=' + event_snapshot['log_msg']

            return self.send_context('eventsnapshot', session_id, event_snapshot, query)
        except Exception:
            our_logger.exception("Error while sending event snapshot %s", self.url)

    def send_context(self, ctx_type, session_id, data, query=''):
        url = self.url + ctx_type + query

        if settings.is_context_debug_enabled():
            our_logger.debug(data)

        data['version'] = self.version
        data['attributes'] = {}

        decorators = dict(self.client_config.decorators)
        for key in decorators.keys():
            decorator = decorators.get(key)
            try:
                name, decorator_data = decorator(data)
                data['attributes'][name] = decorator_data
            except:
                our_logger.exception("Decorator %s %s errored; removing.", key, decorator)
                self.client_config.remove_decorator(key)

        return self.pool.submit(self.pool_task, url, session_id, data)

    def pool_task(self, url, session_id, data):
        our_logger.debug('Task running in pool')
        response = requests.post(url=url, auth=(session_id, self.api_key), json=data)
        json = response.text
        our_logger.debug("Context response: %s", json)
        response.close()

    def send_skipped(self, skipped, session_id):
        return self.send_context('skipped', session_id, skipped)

    def send_profile(self, profile, session_id):
        return self.send_context("profile", session_id, profile)
