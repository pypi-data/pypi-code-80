import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import harp_gate_client.settings as settings
import json


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')

        with open(settings.PATH_TO_MS_CONFIG) as json_file:
            data = json.load(json_file)

        print(data)


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
