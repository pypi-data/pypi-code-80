from unittest import mock

import pytest


@pytest.fixture(scope="session")
def hub(hub):
    for dyne in {{cookiecutter.dyne_list}}:
        hub.pop.sub.add(dyne_name=dyne)

    with mock.patch("sys.argv", ["{{cookiecutter.project_name}}"]):
        hub.pop.config.load(
            {{cookiecutter.dyne_list}},
            cli="{{cookiecutter.clean_name}}",
            parse_cli=True,
        )

    yield hub
