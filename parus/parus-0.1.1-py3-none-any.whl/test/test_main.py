import pytest

from dataclasses import dataclass
from unittest.mock import Mock

from parus.main import main

DUMMY_CREDENTIALS = 'my credentials'
DUMMY_FILE = 'path/to/file'
DUMMY_FILE_ID = 'dummy-file-id'


def search_files_args(query=None, max_size=50, paging=False, page_size=20, credentials=DUMMY_CREDENTIALS):
    return {
        'query': query,
        'max_size': max_size,
        'paging': paging,
        'page_size': page_size,
        'credentials': credentials,
    }


class TestSearchFiles:
    def test_return_zero(self):
        ret = main(['search'])
        assert ret == 0

    @pytest.mark.parametrize('cmd_args, exe_args', [
        ([], search_files_args()),
        *[([a, "name = 'foo'"], search_files_args(query="name = 'foo'")) for a in ['-q', '--query']],
        (['--paging'], search_files_args(paging=True)),
        *[([a, '5'], search_files_args(page_size=5)) for a in ['-p', '--page-size']],
    ])
    def test_with_args(self, subcommand, credentials, cmd_args, exe_args):
        main(['search'] + cmd_args)
        subcommand.search_files.assert_called_once_with(**exe_args)
        credentials.assert_called_once_with(None)

    def test_with_credentials(self, credentials):
        main(['search', '--credentials', 'path/to/credentials'])
        credentials.assert_called_once_with('path/to/credentials')


def upload_to_drive_args(file=DUMMY_FILE, name=None, mime=None, folder_id=None, credentials=DUMMY_CREDENTIALS):
    return {
        'file': file,
        'name': name,
        'mime': mime,
        'folder_id': folder_id,
        'credentials': credentials,
    }


class TestUploadToDrive:
    def test_return_zero(self):
        ret = main(['upload', 'dummy'])
        assert ret == 0

    @pytest.mark.parametrize('cmd_args, exe_args', [
        ([], upload_to_drive_args()),
        (['--name', 'specific file name'], upload_to_drive_args(name='specific file name')),
        (['--mime', 'image/png'], upload_to_drive_args(mime='image/png')),
        (['--folder-id', 'folder-to-upload'], upload_to_drive_args(folder_id='folder-to-upload')),
    ])
    def test_with_args(self, subcommand, credentials, cmd_args, exe_args):
        main(['upload', DUMMY_FILE] + cmd_args)
        subcommand.upload_to_drive.assert_called_once_with(**exe_args)
        credentials.assert_called_once_with(None)

    def test_with_credentials(self, credentials):
        main(['upload', DUMMY_FILE, '--credentials', 'path/to/credentials'])
        credentials.assert_called_once_with('path/to/credentials')


def update_file_args(file=DUMMY_FILE, file_id=DUMMY_FILE_ID, credentials=DUMMY_CREDENTIALS):
    return {
        'file': file,
        'file_id': file_id,
        'credentials': credentials,
    }


class TestUpdateFile:
    def test_return_zero(self):
        ret = main(['update', 'dummy', '--file-id', DUMMY_FILE_ID])
        assert ret == 0

    def test_with_args(self, subcommand, credentials):
        main(['update', DUMMY_FILE, '--file-id', DUMMY_FILE_ID])
        subcommand.update_file.assert_called_once_with(**update_file_args())
        credentials.assert_called_once_with(None)

    def test_with_credentials(self, credentials):
        main(['update', DUMMY_FILE, '--file-id', DUMMY_FILE_ID, '--credentials', 'path/to/credentials'])
        credentials.assert_called_once_with('path/to/credentials')


@pytest.fixture(autouse=True)
def credentials(mocker):
    return mocker.patch('parus.main.get_credentials', return_value=DUMMY_CREDENTIALS)


@pytest.fixture(autouse=True)
def subcommand(mocker):
    @dataclass
    class Subcommands:
        search_files: Mock
        upload_to_drive: Mock
        update_file: Mock

    return Subcommands(
        mocker.patch('parus.main.search_files'),
        mocker.patch('parus.main.upload_to_drive'),
        mocker.patch('parus.main.update_file'))
