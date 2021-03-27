import pytest
from dataclasses import dataclass
from typing import Any


@pytest.fixture
def google_drive_api(mocker):
    @dataclass
    class DriveServiceMocker:
        mocker: Any

        def mock_drive_service_files(self, ds):
            df = self.mocker.Mock()
            self.mocker.patch.object(ds, 'files', return_value=DriveServiceFilesMock(df))
            return df

        def mock_drive_files_create_and_execute(self, df, file_id='file-id', name='file-name'):
            res = {
                'id': file_id,
                'name': name,
            }
            req = self.mocker.Mock()
            self.mocker.patch.object(req, 'execute', return_value=res)
            self.mocker.patch.object(df, 'create', return_value=req)
            return req

        def mock_drive_files_update(self, df, file_id='file-id', name='file-name'):
            res = {
                'id': file_id,
                'name': name,
            }
            req = self.mocker.Mock()
            self.mocker.patch.object(req, 'execute', return_value=res)
            self.mocker.patch.object(df, 'update', return_value=req)
            return req

        def dummy_credentials(self):
            return self.mocker.Mock()

        def mock_build_google_drive_service(self, mod):
            drive_service = self.mocker.Mock()
            return drive_service, self.mocker.patch(f'{mod}.build_google_drive_service', return_value=drive_service)

        def mock_media_file_upload(self, mod):
            mfu = self.mocker.Mock()
            return mfu, self.mocker.patch(f'{mod}.MediaFileUpload', return_value=mfu)

        def mock_drive_files_list(self, df, results=None):
            res = results or [self.drive_files_list_result()]
            req = self.mocker.Mock()
            self.mocker.patch.object(req, 'execute', side_effect=res)
            self.mocker.patch.object(df, 'list', return_value=req)
            return req

        DUMMY_LIST_RESULT_FILES = [{
            'id': f'{i}',
            'name': f'name-{i}',
            'mimeType': f'mime-{i}',
            'trashed': False,
        } for i in range(3)]

        @property
        def dummy_list_result_files(self):
            return DriveServiceMocker.DUMMY_LIST_RESULT_FILES

        def drive_files_list_result(self, files=None, token=None):
            return {
                'files': files or self.dummy_list_result_files,
                'nextPageToken': token,
            }

        def list_params(self, **overrides):
            args = {
                'q': self.mocker.ANY,
                'pageSize': self.mocker.ANY,
                'pageToken': self.mocker.ANY,
                'fields': self.mocker.ANY,
            }
            args.update(**overrides)
            return args

    return DriveServiceMocker(mocker)


@dataclass
class DriveServiceFilesMock:
    drive_files: Any

    def __enter__(self):
        return self.drive_files

    def __exit__(self, *args, **kwargs):
        pass
