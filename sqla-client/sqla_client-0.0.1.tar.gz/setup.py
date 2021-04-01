# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqla_client', 'sqla_client.examples']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['clone-dashboard-and-queries = '
                     'sqla_client.examples.clone_dashboard_and_queries:main',
                     'export-queries = sqla_client.examples.query_export:main']}

setup_kwargs = {
    'name': 'sqla-client',
    'version': '0.0.1',
    'description': 'SQL Analytics API client and tools to manage your instance.',
    'long_description': None,
    'author': 'Databricks Engineering',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
