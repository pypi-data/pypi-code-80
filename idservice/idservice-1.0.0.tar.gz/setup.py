# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idservice']

package_data = \
{'': ['*']}

install_requires = \
['configprops>=1.4.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'mypy>=0.812,<0.813',
 'uvicorn[standard]>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'idservice',
    'version': '1.0.0',
    'description': 'Distributed ID generator microservice based on FastAPI',
    'long_description': None,
    'author': 'Xu Yijun',
    'author_email': 'xuyijun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tommyxu/idservice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
