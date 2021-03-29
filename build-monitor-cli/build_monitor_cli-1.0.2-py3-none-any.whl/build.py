from dataclasses import dataclass
from typing import List, Optional, Callable, Any, Iterable, Mapping
from threading import Thread
from time import sleep, time
from rich.spinner import Spinner

build_store = None

@dataclass
class Build:
    name: str
    path: str
    build_number: str
    status: str
    requested_by: str
    requested_by_uniq: str
    repo_id: str
    source_branch: str
    source_version: str

    def get_requested_by(self):
        return f'{self.requested_by} ({self.requested_by_uniq})'
    
    def render_status(self):
        if self.status == 'processing':
            return Spinner('dots', 'processing')
        return self.status

def get_value(obj, property_name):
    if '.' not in property_name:
        return getattr(obj, property_name)
    property_names = property_name.split('.')
    return get_value(get_value(obj, property_names[0]), '.'.join(property_names[1:]))

def extract_status(build: Build):
    if build.status == 'inProgress':
        return 'processing'
    return build.result

def list_builds(build_client, proj_name, branch) -> List[Build]:
    global build_store
    if build_store:
        return build_store
    
    update_build_store(build_client, proj_name, branch)
    if not build_store:
        raise Exception('can not initialize build store')
    
    return build_store

def update_build_store(build_client, proj_name, branch):
    try:
        resp = build_client.get_builds(proj_name, max_builds_per_definition=1, branch_name=f'refs/heads/{branch}', query_order='queueTimeDescending')
    except Exception:
        pass
    else:
        global build_store
        build_store = [Build(
                get_value(build, 'definition.name'),
                get_value(build, 'definition.path'),
                get_value(build, 'build_number'),
                extract_status(build),
                get_value(build, 'requested_for.display_name'),
                get_value(build, 'requested_for.unique_name'),
                get_value(build, 'repository.id'),
                get_value(build, 'source_branch'),
                get_value(build, 'source_version'),
                )
                for build in resp]

class BuildUpdater(Thread):
    def __init__(self, args) -> None:
        super().__init__(group=None, target=None, name=None, args=args, kwargs={})
        self.args = args
        self.stopped = False
    
    def stop(self):
        self.stopped = True

    def run(self) -> None:
        start_time = time()
        client, proj_name, branch = self.args
        while not self.stopped:
            if time() - start_time > 30:
                update_build_store(client, proj_name, branch)
                start_time = time()
            sleep(.5)