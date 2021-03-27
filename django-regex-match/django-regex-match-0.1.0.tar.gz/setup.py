# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['regex_match',
 'regex_match.migrations',
 'regex_match.models',
 'regex_match.objects',
 'regex_match.objects.parsers']

package_data = \
{'': ['*'], 'regex_match': ['fixtures/*']}

setup_kwargs = {
    'name': 'django-regex-match',
    'version': '0.1.0',
    'description': 'A URL match and classification engine',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
