# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ip_object_browser']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=20.2.1,<21.0.0', 'ipython>=7.21.0,<8.0.0', 'urwid>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'ip-object-browser',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Roee Nizan',
    'author_email': 'roeen30@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
