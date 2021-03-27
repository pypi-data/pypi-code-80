import pathlib
import pytest
from dataclasses import dataclass
from typing import Any

import parus.config as config


@pytest.fixture
def parus_config(mocker):
    @dataclass
    class ParusConfigMocker:
        mocker: Any

        def mock_get_default_credentials_file(self, credentials_file=None):
            return self.mocker.patch('parus.auth.get_default_credentials_file', return_value=credentials_file)

        def mock_token_file_for(self, token_file=None):
            return self.mocker.patch('parus.auth.token_file_for', return_value=token_file)

        def mock_default_credentials_ang_token(self, home_dir, create_creds=True, create_token=True):
            parus_dir = self.create_parus_dir(home_dir)
            creds_file, token_file = self.set_up_creds_files(
                parus_dir, create_creds=create_creds, create_token=create_token)
            return (
                creds_file,
                token_file,
                self.mock_get_default_credentials_file(creds_file),
                self.mock_token_file_for(token_file),
            )

        def set_up_creds_files(self, directory, create_creds=False, create_token=False):
            directory.mkdir(exist_ok=True)
            creds_file = directory / 'creds.json'
            token_file = directory / 'token.json'
            if create_creds:
                with open(creds_file, 'w'):
                    pass
            if create_token:
                with open(token_file, 'w'):
                    pass
            return creds_file, token_file

        def create_dummy_properties(self, p_file):
            conf = config.Configuration(
                default=config.Properties(
                    folder_id='default-folder-id'))
            self.create_properties_file(p_file, conf)

        def create_properties_file(self, p_file, configuration=None, force=False):
            if configuration is not None:
                configuration.save(p_file)
            elif force:
                with open(p_file, 'w'):
                    pass
            if p_file.exists():
                with open(p_file) as fp:
                    lines = [l for l in [l.rstrip() for l in fp] if l]
                    print(f'properties for test saved: {lines}')

            return p_file

        def create_parus_dir(self, home_dir):
            parus_dir = pathlib.Path(home_dir, '.parus')
            parus_dir.mkdir(parents=True, exist_ok=True)
            return parus_dir

        def mock_get_default_folder_id(self, mod, folder_id=None):
            return self.mocker.patch(f'{mod}.get_default_folder_id', return_value=folder_id)

    return ParusConfigMocker(mocker)
