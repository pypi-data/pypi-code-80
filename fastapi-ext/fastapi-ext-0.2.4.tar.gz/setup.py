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
    'version': '0.2.4',
    'description': 'FastAPI extensions focused on productivity',
    'long_description': '# fastapi-ext\n\n[![CI](https://github.com/dlski/fastapi-ext/workflows/CI/badge.svg)](https://github.com/dlski/fastapi-ext/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)\n[![codecov](https://codecov.io/gh/dlski/fastapi-ext/branch/main/graph/badge.svg?token=YZJDTRQ5M7)](https://codecov.io/gh/dlski/fastapi-ext)\n[![pypi](https://img.shields.io/pypi/v/fastapi-ext.svg)](https://pypi.python.org/pypi/fastapi-ext)\n[![downloads](https://img.shields.io/pypi/dm/fastapi-ext.svg)](https://pypistats.org/packages/fastapi-ext)\n[![versions](https://img.shields.io/pypi/pyversions/fastapi-ext.svg)](https://github.com/dlski/fastapi-ext)\n[![license](https://img.shields.io/github/license/dlski/fastapi-ext.svg)](https://github.com/dlski/fastapi-ext/blob/master/LICENSE)\n\n\nFastAPI extensions focused on productivity, contains:\n* `View` class to replace plain function binding within router (with counterparts decorators)\n* simple `AuthCheckDependency` to validate privileges\n\n## Help\nComing soon...\n',
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
