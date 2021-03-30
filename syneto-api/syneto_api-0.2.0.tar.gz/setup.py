# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['syneto_api']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.16.0,<0.17.0', 'requests[secure]>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'syneto-api',
    'version': '0.2.0',
    'description': 'Syneto Client API library',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
