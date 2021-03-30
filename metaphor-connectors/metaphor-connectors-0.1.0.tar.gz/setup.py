# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metaphor',
 'metaphor.common',
 'metaphor.dbt_extractor',
 'metaphor.postgresql',
 'metaphor.snowflake_extractor']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.19,<1.18.0',
 'botocore>=1.20.19,<1.21.0',
 'fastjsonschema>=2.15.0,<2.16.0',
 'python-dateutil>=2.8.1,<2.9.0']

extras_require = \
{'all': ['asyncpg>=0.22.0,<0.23.0', 'snowflake-connector-python>=2.4.1,<2.5.0'],
 'postgresql': ['asyncpg>=0.22.0,<0.23.0'],
 'snowflake': ['snowflake-connector-python>=2.4.1,<2.5.0']}

setup_kwargs = {
    'name': 'metaphor-connectors',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Metaphor',
    'author_email': 'dev@metaphor.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
