# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idservice']

package_data = \
{'': ['*']}

install_requires = \
['configprops>=1.4.0,<2.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'uvicorn[standard]>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['idservice-start = idservice.__main__:main']}

setup_kwargs = {
    'name': 'idservice',
    'version': '1.2.2',
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
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
