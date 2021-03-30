# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_run_dt']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2.0']

setup_kwargs = {
    'name': 'code-run-dt',
    'version': '0.2.0',
    'description': 'Code Run Data Type',
    'long_description': '# code run data type\n\nCode Run Data Definition\n\n## WARNING\n\n    may useless to you\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.qiyutech.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
