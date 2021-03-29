# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['incompatible_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'incompatible-library',
    'version': '2.0.0',
    'description': 'An example of a library which has incompatible changes from one version to the next',
    'long_description': None,
    'author': 'Jordan Gillard',
    'author_email': 'jordan-gillard@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
