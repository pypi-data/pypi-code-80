# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cepan']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.19,<2.0.0', 'pandas>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'cepan',
    'version': '0.1.0',
    'description': 'Retrieves data from aws cost explore as a pandas dataframe.',
    'long_description': '# cepan\n\n[![test](https://github.com/kanga333/cepan/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/test.yml)\n[![lint](https://github.com/kanga333/cepan/actions/workflows/lint.yml/badge.svg?branch=main)](https://github.com/kanga333/cepan/actions/workflows/lint.yml)\n[![Code style: black](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n\nRetrieves data from aws cost explore as a pandas dataframe.\n\nMain features\n- Support for input with type hints\n- Retrieving results as pandas.Dataframe\n\n## Installation\n\n```\npip install cepan\n```\n\n## Usage\n\n```python\nfrom datetime import datetime\n\nimport cepan as ce\n\ndf = ce.get_cost_and_usage(\n    time_period=ce.TimePeriod(\n        start=datetime(2020, 1, 1),\n        end=datetime(2020, 1, 2),\n    ),\n    granularity="DAILY",\n    filter=ce.And(\n        [\n            ce.Dimensions(\n                "SERVICE",\n                ["Amazon Simple Storage Service", "AmazonCloudWatch"],    \n            ),\n            ce.Tags("Stack", ["Production"]),\n        ]\n    ),\n    metrics=["BLENDED_COST"],\n    group_by=ce.GroupBy(\n        dimensions=["SERVICE", "USAGE_TYPE"],\n    ),\n)\nprint(df)\n```\n\nAll paginated results will be returned as a Dataframe.\n\n```\n          Time                        SERVICE  BlendedCost\n0   2020-01-01  Amazon Simple Storage Service   100.000000\n1   2020-01-01               AmazonCloudWatch    10.000000\n```\n\n### List of currently supported APIs\n\n- get_dimension_values\n- get_tags\n- get_cost_and_usage\n\n## License\n\nMIT License\n',
    'author': 'kanga333',
    'author_email': 'e411z7t40w@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
