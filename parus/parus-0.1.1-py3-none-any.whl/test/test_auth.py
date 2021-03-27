import pathlib

import pytest

from dataclasses import dataclass
from typing import Any

from parus.auth import get_credentials

SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]


class TestGetCredentials:
    class TestValidCredentials:
        def test_from_default(self, tmpdir, google_auth_api, parus_config):
            valid_creds = google_auth_api.mock_credentials(valid=True)
            load_creds = google_auth_api.mock_load_credentials(credentials=valid_creds)

            mocks = parus_config.mock_default_credentials_ang_token(tmpdir)
            creds_file, token_file, get_deafult_creds_file, token_file_for = mocks

            creds = get_credentials()

            assert creds == valid_creds
            get_deafult_creds_file.assert_called_once()
            token_file_for.assert_called_once_with(creds_file)
            load_creds.assert_called_once_with(token_file, SCOPES)

        def test_from_specified(self, tmpdir, google_auth_api, parus_config):
            work_dir = pathlib.Path(tmpdir, 'work')
            creds_file, token_file = parus_config.set_up_creds_files(work_dir, create_creds=True, create_token=True)
            get_deafult_creds_file = parus_config.mock_get_default_credentials_file()
            token_file_for = parus_config.mock_token_file_for(token_file)

            valid_creds = google_auth_api.mock_credentials(valid=True)
            load_creds = google_auth_api.mock_load_credentials(credentials=valid_creds)

            creds = get_credentials(creds_file)

            assert creds == valid_creds
            get_deafult_creds_file.asert_not_called()
            token_file_for.assert_called_once_with(creds_file)
            load_creds.assert_called_once_with(token_file, SCOPES)

    class TestRefreshToken:
        def test_refresh(self, tmpdir, google_auth_api, parus_config):
            parus_config.mock_default_credentials_ang_token(tmpdir)

            refreshable_creds = google_auth_api.mock_credentials(
                valid=False,
                expired=True,
                refresh_token='refresh token',
                to_json='token json')
            google_auth_api.mock_load_credentials(credentials=refreshable_creds)
            request, request_mock = google_auth_api.mock_request()

            creds = get_credentials()

            assert creds == refreshable_creds
            request_mock.assert_called_once()
            refreshable_creds.refresh.assert_called_once_with(request)

        def test_save_refreshed_token(self, tmpdir, google_auth_api, parus_config):
            refreshable_creds = google_auth_api.mock_credentials(
                valid=False,
                expired=True,
                refresh_token='refresh token',
                to_json='token json')
            google_auth_api.mock_load_credentials(credentials=refreshable_creds)
            google_auth_api.mock_request()

            _, token_file, _, _ = parus_config.mock_default_credentials_ang_token(tmpdir)

            get_credentials()

            with open(token_file) as fp:
                assert fp.read() == 'token json'

    class TestCreateNewToken:
        def test_when_unrefreshable(self, tmpdir, google_auth_api, parus_config):
            invalid_creds_file, token_file, _, _ = parus_config.mock_default_credentials_ang_token(tmpdir)

            invalid_creds = google_auth_api.mock_credentials(
                valid=False,
                expired=True,
                refresh_token=None)
            google_auth_api.mock_load_credentials(credentials=invalid_creds)
            _, new_creds, flow_from_secrets, run_flow_server = google_auth_api.mock_creds_from_flow()

            creds = get_credentials()

            assert creds == new_creds
            flow_from_secrets.assert_called_once_with(invalid_creds_file, SCOPES)
            run_flow_server.assert_called_once_with(port=0)

        def test_when_token_not_created_yet(self, tmpdir, google_auth_api, parus_config):
            creds_file, token_file, _, _ = parus_config.mock_default_credentials_ang_token(tmpdir, create_token=False)

            load_creds = google_auth_api.mock_load_credentials()
            _, new_creds, flow_from_secrets, run_flow_server = google_auth_api.mock_creds_from_flow()

            creds = get_credentials()

            assert creds == new_creds
            load_creds.assert_not_called()
            flow_from_secrets.assert_called_once_with(creds_file, SCOPES)
            run_flow_server.assert_called_once_with(port=0)

        def test_save_new_token(self, tmpdir, google_auth_api, parus_config):
            _, token_file, _, _ = parus_config.mock_default_credentials_ang_token(tmpdir)

            invalid_creds = google_auth_api.mock_credentials(
                valid=False,
                expired=True,
                refresh_token=None)
            google_auth_api.mock_load_credentials(credentials=invalid_creds)
            google_auth_api.mock_creds_from_flow(token_json='new token json')

            get_credentials()

            with open(token_file) as fp:
                assert fp.read() == 'new token json'

    class TestError:
        def test_when_default_credentials_file_not_found(self, tmpdir, parus_config):
            creds_file, _, _, _ = parus_config.mock_default_credentials_ang_token(tmpdir, create_creds=False)

            with pytest.raises(RuntimeError) as e:
                get_credentials()

            assert str(e.value) == ('Credentials file not found.'
                                    ' Specify by --credentials option,'
                                    ' or put credentials.json in $HOME/.parus/')

        def test_when_specified_credentials_file_not_found(self, tmpdir, parus_config):
            work_dir = pathlib.Path(tmpdir, 'work')
            creds_file, _ = parus_config.set_up_creds_files(work_dir, create_creds=False)

            with pytest.raises(RuntimeError) as e:
                get_credentials(creds_file)

            assert str(e.value) == ('Credentials file not found.'
                                    ' Specify by --credentials option,'
                                    ' or put credentials.json in $HOME/.parus/')


@pytest.fixture
def google_auth_api(mocker):
    @dataclass
    class GoogleAuthApiMocker:
        mocker: Any

        def mock_load_credentials(self, credentials=None):
            return self.mocker.patch('parus.auth.Credentials.from_authorized_user_file', return_value=credentials)

        def mock_request(self):
            request = self.mocker.Mock()
            return request, self.mocker.patch('parus.auth.Request', return_value=request)

        def mock_creds_from_flow(self, token_json='token json'):
            flow = self.mocker.Mock()
            creds = self.mock_credentials(to_json=token_json)
            flow_from_secrets = self.mocker.patch('parus.auth.InstalledAppFlow.from_client_secrets_file',
                                                  return_value=flow)
            run_flow_server = self.mocker.patch.object(flow, 'run_local_server', return_value=creds)
            return flow, creds, flow_from_secrets, run_flow_server

        def mock_credentials(self, valid=None, expired=None, refresh_token=None, to_json=None):
            creds = self.mocker.Mock()
            self.mocker.patch.object(creds, 'valid', valid)
            self.mocker.patch.object(creds, 'expired', expired)
            self.mocker.patch.object(creds, 'refresh_token', refresh_token)
            if to_json is not None:
                self.mocker.patch.object(creds, 'to_json', return_value=to_json)
            return creds

    return GoogleAuthApiMocker(mocker)
