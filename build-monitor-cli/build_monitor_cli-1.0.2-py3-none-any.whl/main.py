import time
import sys
import os
from typing import List
import threading
from azure.devops.connection import Connection
from github import Github
from msrest.authentication import BasicAuthentication
from rich.console import Console
from rich.table import Table
from rich.live import Live
from build_monitor_cli.build import Build, list_builds, BuildUpdater
from build_monitor_cli.config import AppConfig

build_updater_thread = None
github_threads = []

def get_client(org_url, pat):
    credentials = BasicAuthentication('', pat)
    connection = Connection(base_url=org_url, creds=credentials)
    
    return connection.clients_v6_0.get_build_client()

def get_github_client(gh_pat):
    return Github(gh_pat)

commit_store = {}
def get_commit_metadata(gh_proj: str, commit_hash: str):
    store_key = (gh_proj, commit_hash)
    return commit_store.get(store_key)


def update_commit_metadata(gh_client, gh_proj, commit_hash):
    store_key = (gh_proj, commit_hash)
    try:
        gh_repo = gh_client.get_repo(gh_proj)
        gh_commit = gh_repo.get_commit(commit_hash)
    except Exception:
        pass
    else:
        metadata = (gh_commit.commit.committer.name, gh_commit.commit.committer.email)
        commit_store[store_key] = metadata


def sort_by_failed(builds: List[Build]) -> List[Build]:
    return sorted(builds, key=lambda b: (b.status is None, b.status != 'failed', b.name))

def get_requested_by(build: Build, gh_client: Github):
    metadata = get_commit_metadata(build.repo_id, build.source_version)
    if not metadata:
        t = threading.Thread(target=update_commit_metadata, args=(gh_client, build.repo_id, build.source_version))
        github_threads.append(t)
        t.start()
        return build.get_requested_by()
    committer_name, committer_email = metadata
    return f'{committer_name} ({committer_email})'

def generate_table(build_client, gh_client, branch, proj_name, dest_path) -> Table:
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('Name')
    table.add_column('Build Number')
    table.add_column('By')
    table.add_column('Status')

    builds = list_builds(build_client, proj_name, branch)
    if dest_path:
        builds = [b for b in builds if b.path == dest_path]
    for build in sort_by_failed(builds):
        table.add_row(build.name, build.build_number, get_requested_by(build, gh_client), build.render_status())
    
    return table

def main(organization, branch):
    try:
        home_path = os.getenv('HOME')
        app_config = AppConfig(f'{home_path}/.config/build_monitor_cli/config.ini', organization)
        build_client = get_client(app_config.get_config('organization_url'), app_config.get_config('personal_access_token'))
        gh_client = get_github_client(app_config.get_config('gh_personal_access_token'))
        
        with Console().status('Initializing...'):
            table = generate_table(build_client, gh_client, branch, app_config.get_config('project_name'), app_config.get_config('dest_path'))
        
        global build_updater_thread
        build_updater_thread = BuildUpdater(args=(build_client, app_config.get_config('project_name'), branch))
        build_updater_thread.start()

        with Live(table, auto_refresh=True) as live:
            while 1:
                live.update(generate_table(build_client, gh_client, branch, app_config.get_config('project_name'), app_config.get_config('dest_path')))
                time.sleep(3)
    except KeyboardInterrupt:
        if build_updater_thread and build_updater_thread.is_alive():
            with Console().status('Terminating build updater...'):
                build_updater_thread.stop()
                build_updater_thread.join()

        alive_github_threads = [t for t in github_threads if t.is_alive()]    
        if alive_github_threads:
            with Console().status('Terminating metadata updater...'):
                for t in alive_github_threads:
                    t.join()
        sys.exit(0)
