# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyforge']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'forge-client',
    'version': '0.1.0',
    'description': 'AutoDesk Forge API Python Client.',
    'long_description': '# pyforge\nAutoDesk Forge API Python Client.\n',
    'author': 'yutayamazaki',
    'author_email': 'tppymd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yutayamazaki/pyforge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
