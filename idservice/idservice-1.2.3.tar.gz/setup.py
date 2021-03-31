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
    'version': '1.2.3',
    'description': 'Distributed ID generator microservice based on FastAPI',
    'long_description': '# idservice\n\n`ID-Service` is a distributed ID generator microservice based on FastAPI.\n\n## Installation\n\n```sh\npip3 install idservice\n```\n\n## Start Service\n\n```sh\nidservice-start\n```\n\n> List all available `uvicorn` options by `idservice-start --help`\n\n## API Endpoint\n\nSeveral endpoints:\n\n-   `/api/snowflake`\n-   `/api/random/64`\n-   `/api/uuid`\n\nBrowse `/docs` (default to http://localhost:8000/docs) to read all APIs.\n\n## Configuration\n\nEnvironment variable:\n\n| Environment Vars                  | Usage                          | Default |\n| --------------------------------- | ------------------------------ | ------- |\n| `ID_SERVICE_SNOWFLAKE_MACHINE_ID` | Snowflake Machine ID (10 bits) | Random  |\n',
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
