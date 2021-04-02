# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnpm', 'pnpm.generator.__pkg__']

package_data = \
{'': ['*'],
 'pnpm': ['generator/docs/*'],
 'pnpm.generator.__pkg__': ['src/*', 'src/icons/*', 'src/styles/*', 'test/*']}

install_requires = \
['numpy>=1.20.1,<2.0.0', 'rglob>=1.7,<2.0', 'rich>=9.13.0,<10.0.0']

setup_kwargs = {
    'name': 'pnpm',
    'version': '0.2.18',
    'description': '',
    'long_description': None,
    'author': 'robo-monk',
    'author_email': 'rrobomonk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
