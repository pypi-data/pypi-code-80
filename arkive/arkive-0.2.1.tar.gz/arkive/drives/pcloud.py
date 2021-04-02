import json
from urllib import request, parse
from pathlib import Path

from arkive.core.drive import Drive


def _pcloud_metadata(track: dict):
    return {key: track[key] for key in ['artist', 'album', 'title', 'path']}


def _pcloud_recurse(root: dict, path: Path):
    for item in root.get('contents', []):
        item['path'] = path / item['name']
        if not item['isfolder'] and item['icon'] == 'audio':
            yield _pcloud_metadata(item)
        yield from _pcloud_recurse(item, item["path"])


def _pcloud_request(action: str, params: dict, auth: dict):
    queries = parse.urlencode({**params, **auth})
    response = request.urlopen(f'https://api.pcloud.com/{action}?{queries}')
    return json.load(response)


def _pcloud_index(path: Path, auth: dict):
    params = {'path': path.as_posix(), 'recursive': True}
    data = _pcloud_request('listfolder', params, auth)
    assert data['result'] is 0, f'STATUS {data["result"]}: {data["error"]}'
    yield from _pcloud_recurse(data['metadata'], path)


def _pcloud_rename(source: Path, dest: Path, auth: dict):
    params = {'path': source.as_posix(), 'topath': dest.as_posix()}
    data = _pcloud_request('renamefile', params, auth)
    assert data['result'] is 0, f'STATUS {data["result"]}: {data["error"]}'


def _pcloud_create_folder(folder: Path, auth: dict):
    params = {'path': folder.as_posix()}
    data = _pcloud_request('createfolderifnotexists', params, auth)
    if data['result'] == 2002:
        _pcloud_create_folder(folder.parent, auth)
        _pcloud_create_folder(folder, auth)
    else:
        assert data['result'] is 0, f'STATUS {data["result"]}: {data["error"]}'


def _pcloud_list_items_recurse(root: dict, path: Path):
    for item in root.get('contents', []):
        item['path'] = path / item['name']
        yield item
        yield from _pcloud_list_items_recurse(item, item["path"])


def _pcloud_list_items(path: Path, auth: dict):
    params = {'path': path.as_posix(), 'recursive': False}
    data = _pcloud_request('listfolder', params, auth)
    assert data['result'] is 0, f'STATUS {data["result"]}: {data["error"]} -> {path}'
    yield from _pcloud_list_items_recurse(data['metadata'], path)


def _pcloud_remove_folder(folder: Path, auth: dict):
    params = {'path': folder.as_posix()}
    _pcloud_request('deletefolder', params, auth)


def _pcloud_cleanup(folder: Path, auth: dict):
    for item in _pcloud_list_items(folder, auth):
        if item['isfolder']:
            _pcloud_cleanup(item['path'], auth)
            _pcloud_remove_folder(item['path'], auth)


class PCloudDrive(Drive):
    def __init__(self, auth: dict):
        self.auth = auth

    def index(self, folder: Path):
        yield from _pcloud_index(folder, self.auth)

    def rename(self, source: Path, dest: Path):
        _pcloud_create_folder(dest.parent, self.auth)
        _pcloud_rename(source, dest, self.auth)

    def cleanup(self, folder: Path):
        _pcloud_cleanup(folder, self.auth)
