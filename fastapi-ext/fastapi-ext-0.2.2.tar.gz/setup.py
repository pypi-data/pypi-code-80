# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_ext', 'fastapi_ext.view', 'fastapi_ext.view.decorators']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.62.0']

setup_kwargs = {
    'name': 'fastapi-ext',
    'version': '0.2.2',
    'description': 'FastAPI extensions focused on productivity',
    'long_description': '# fastapi-ext\n\nFastAPI extensions focused on productivity, contains:\n* `View` class to replace plain function binding within router (with counterparts decorators)\n* simple `AuthCheckDependency` to validate privileges\n\n## Help\nComing soon...\n',
    'author': 'Damian Łukawski',
    'author_email': 'damian@lukawscy.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dlski/fastapi-ext',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
