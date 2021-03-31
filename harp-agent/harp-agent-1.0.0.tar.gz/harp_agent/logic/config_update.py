import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import harp_agent.settings as settings
import json


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')

        with open(settings.PATH_TO_MS_CONFIG) as json_file:
            data = json.load(json_file)

        for system_name, system_body in data.items():
            system_payload = {
                'url': system_body['url'],
                'user': system_body['user'],
                'password': system_body['password']
            }
            if system_body['monitoring_system'] == 'zabbix':
                settings.ZABBIX_SYSTEMS.clear()
                settings.ZABBIX_SYSTEMS.append(system_payload)

            if system_body['monitoring_system'] == 'icinga':
                settings.ICINGA_SYSTEMS.clear()
                settings.ICINGA_SYSTEMS.append(system_payload)

        print(f"ZABBIX_SYSTEMS: {settings.ZABBIX_SYSTEMS}")
        print(f"ICINGA_SYSTEMS: {settings.ICINGA_SYSTEMS}")


def update_configuration():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=settings.PATH_TO_MS_CONFIG, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
