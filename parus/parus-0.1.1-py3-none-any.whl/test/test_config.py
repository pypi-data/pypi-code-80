import configparser
import pathlib

import pytest

import parus.config as config

DUMMY_PARUS_DIR = pathlib.Path('home', '.parus')


def test_default_credentials_file():
    default_creds_file = pathlib.Path.home().joinpath('.parus', 'credentials.json')

    creds_file = config.get_default_credentials_file()

    assert creds_file == default_creds_file


def test_token_file_from():
    creds_file = DUMMY_PARUS_DIR.joinpath('credentials.json')

    token_file = config.token_file_for(creds_file)

    assert token_file == DUMMY_PARUS_DIR.joinpath('google-api-token.json')


class TestDefaultConfiguration:
    class TestGetDefaultFolder:
        def test_load_default_folder(self, parus_config, parus_properties):
            conf = config.Configuration(
                default=config.Properties(
                    folder_id='default-folder-id'))
            parus_config.create_properties_file(parus_properties, configuration=conf)

            folder_id = config.get_default_folder_id()

            assert folder_id == 'default-folder-id'

        @pytest.mark.parametrize('conf', [
            config.Configuration(default=config.Properties(folder_id=None)),
            config.Configuration(default=None),
            None,
        ])
        def test_no_default_folder(self, conf, parus_properties, parus_config):
            parus_config.create_properties_file(parus_properties, configuration=conf)

            folder_id = config.get_default_folder_id()

            assert folder_id is None


class TestConfiguration:
    class TestLoad:
        def test_load_configuration(self, parus_properties):
            c = configparser.ConfigParser()
            c['DEFAULT'] = {
                'folder-id': 'xxx',
            }
            with open(parus_properties, 'w') as fp:
                c.write(fp)

            loaded_conf = config.Configuration.load(parus_properties)

            assert loaded_conf == config.Configuration(
                default=config.Properties(
                    folder_id='xxx'))

    class TestSave:
        def test_save_configuration(self, parus_properties):
            c = config.Configuration(
                default=config.Properties(folder_id='xxx'))

            c.save(parus_properties)

            saved = read_properties_file(parus_properties)
            assert saved['DEFAULT']['folder-id'] == 'xxx'

        @pytest.mark.parametrize('default_prop', [
            config.Properties(folder_id=None),
            None,
        ])
        def test_clear_default_property_when_none(
                self, default_prop, parus_config, parus_properties):
            parus_config.create_dummy_properties(parus_properties)
            c = config.Configuration(default=default_prop)

            c.save(parus_properties)

            saved = read_properties_file(parus_properties)
            assert not_in_config(saved, 'DEFAULT', 'folder-id')


def read_properties_file(f):
    c = configparser.ConfigParser()
    with open(f) as fp:
        c.read_string(fp.read())
    return c


def not_in_config(c, section, prop):
    return section not in c or prop not in c[section]


@pytest.fixture
def home_dir(mocker, tmpdir):
    home_dir = pathlib.Path(tmpdir, 'home')
    mocker.patch('pathlib.Path.home', return_value=home_dir)
    return home_dir


@pytest.fixture
def parus_dir(parus_config, home_dir):
    return parus_config.create_parus_dir(home_dir)


@pytest.fixture
def parus_properties(parus_dir):
    return pathlib.Path(parus_dir, 'parus.properties')
