# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['homeassistant-stubs']

package_data = \
{'': ['*'],
 'homeassistant-stubs': ['auth/*',
                         'auth/mfa_modules/*',
                         'auth/permissions/*',
                         'auth/providers/*',
                         'components/*',
                         'components/automation/*',
                         'components/binary_sensor/*',
                         'components/bond/*',
                         'components/calendar/*',
                         'components/cover/*',
                         'components/device_automation/*',
                         'components/frontend/*',
                         'components/geo_location/*',
                         'components/group/*',
                         'components/history/*',
                         'components/http/*',
                         'components/huawei_lte/*',
                         'components/hyperion/*',
                         'components/image_processing/*',
                         'components/integration/*',
                         'components/knx/*',
                         'components/light/*',
                         'components/lock/*',
                         'components/mailbox/*',
                         'components/media_player/*',
                         'components/notify/*',
                         'components/number/*',
                         'components/persistent_notification/*',
                         'components/proximity/*',
                         'components/recorder/*',
                         'components/remote/*',
                         'components/scene/*',
                         'components/sensor/*',
                         'components/slack/*',
                         'components/sun/*',
                         'components/switch/*',
                         'components/systemmonitor/*',
                         'components/tts/*',
                         'components/vacuum/*',
                         'components/water_heater/*',
                         'components/weather/*',
                         'components/websocket_api/*',
                         'components/zeroconf/*',
                         'components/zone/*',
                         'components/zwave_js/*',
                         'helpers/*',
                         'scripts/*',
                         'scripts/benchmark/*',
                         'scripts/macos/*',
                         'util/*',
                         'util/yaml/*']}

install_requires = \
['homeassistant==2021.4.0b3']

setup_kwargs = {
    'name': 'homeassistant-stubs',
    'version': '2021.4.0b3',
    'description': 'PEP 484 typing stubs for Home Assistant Core',
    'long_description': "# PEP 484 stubs for Home Assistant Core\n\n[![CI](https://github.com/KapJI/homeassistant-stubs/actions/workflows/ci.yaml/badge.svg)](https://github.com/KapJI/homeassistant-stubs/actions/workflows/ci.yaml)\n[![PyPI version](https://badge.fury.io/py/homeassistant-stubs.svg)](https://pypi.org/project/homeassistant-stubs/)\n\nThis is unofficial stub-only package generated from [Home Assistant Core](https://github.com/home-assistant/core) sources.\nYou can use it to enable type checks against Home Assistant code in your custom component or AppDaemon apps.\n\n## How to use\n\nAdd it to dev dependencies of your project.\nI recommend to use [Poetry](https://python-poetry.org/) for managing dependencies:\n\n```shell\npoetry add --dev homeassistant-stubs\n```\n\nPlease note that only stubs from strictly typed modules are added in this package.\nThis includes all core modules and some components.\nGeneric components like `sensor`, `light` or `media_player` are already typed.\n\nIf your project imports not yet typed components, `mypy` will be unable to find that module.\nThe best thing you can do to fix this is to submit PR to HA Core which adds type hints for these components.\nAfter that stubs for these components will become available in this package.\n\n## Motivation\n\nHome Assistant maintainers don't want to distribute typing information with `homeassistant` package\n([[1]](https://github.com/home-assistant/core/pull/28866),\n[[2]](https://github.com/home-assistant/core/pull/47796)).\nThe reason is that [PEP 561](https://www.python.org/dev/peps/pep-0561/#packaging-type-information)\nsays that `py.typed` marker is applied recursively and the whole package must support type checking.\nBut many of the Home Assistant components are currently not type checked.\n\n## How it works\n\n- `update_stubs.py` script extracts list of strictly typed modules from Home Assistant `setup.cfg`.\n- Then it runs `stubgen` which is shipped with `mypy` to generate typing stubs.\n",
    'author': 'Ruslan Sayfutdinov',
    'author_email': 'ruslan@sayfutdinov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KapJI/homeassistant-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
