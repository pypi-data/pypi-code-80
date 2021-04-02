# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asy']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'asy',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
