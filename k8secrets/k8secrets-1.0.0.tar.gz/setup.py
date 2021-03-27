# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['k8secrets']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['k8secrets = k8secrets.__main__:main']}

setup_kwargs = {
    'name': 'k8secrets',
    'version': '1.0.0',
    'description': 'Generate Kubernetes Configs and Secrets from a list of environment variables',
    'long_description': None,
    'author': 'Max K.',
    'author_email': 'kovykmax@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luminaar/k8secret',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
