# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic', 'platonic.sqs', 'platonic.sqs.queue']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'boltons>=20.2.1,<21.0.0',
 'boto3-stubs[sqs]>=1.15.10,<2.0.0',
 'boto3>=1.17.15,<2.0.0',
 'botocore>=1.20.15,<2.0.0',
 'mypy-boto3-sqs>=1.17.26,<2.0.0',
 'platonic>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'platonic-sqs',
    'version': '1.2.7',
    'description': 'Platonic wrapper for Amazon Simple Queue Service',
    'long_description': "# platonic-sqs\n\n[![Coverage](https://coveralls.io/repos/github/python-platonic/platonic-sqs/badge.svg?branch=master)](https://coveralls.io/github/python-platonic/platonic-sqs?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/platonic-sqs.svg)](https://pypi.org/project/platonic-sqs/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nA [platonic](https://platonic.tools) wrapper for Amazon SQS queue service. Abstracts away the implementation details of SQS, providing you with a clean and typed queue interface.\n\n\n## Installation\n\n```bash\npip install platonic-sqs\n```\n\n\n## Send\n\n```python\nfrom platonic.sqs.queue import SQSSender\n\nnumbers_out = SQSSender[int](\n    url='https://sqs.us-west-2.amazonaws.com/123456789012/queue-name',\n)\n\nnumbers_out.send(15)\nnumbers_out.send_many([1, 1, 2, 3, 5, 8, 13])\n```\n\n## Receive & acknowledge\n\n```python\nfrom platonic.sqs.queue import SQSReceiver\nfrom platonic.timeout import ConstantTimeout\nfrom datetime import timedelta\n\nincoming_numbers = SQSReceiver[int](\n    url='https://sqs.us-west-2.amazonaws.com/123456789012/queue-name',\n    # Thus we prevent the receiver from blocking forever if queue is empty\n    timeout=ConstantTimeout(period=timedelta(minutes=3)),\n)\n\n# If the queue is empty, this call with block until there is a message.\ncmd = incoming_numbers.receive()\n\nassert cmd.value == 15\n# Do complicated stuff with the value\nprint(cmd.value * 1234 + 5767)\n\nincoming_numbers.acknowledge(cmd)\n```\n\n## License\n\n[MIT](https://github.com/python-platonic/platonic-sqs/blob/master/LICENSE)\n\n\n## Credits\n\n* This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [c9e9ea8b9be2464cacd00b9c2a438e821da9121b](https://github.com/wemake-services/wemake-python-package/tree/c9e9ea8b9be2464cacd00b9c2a438e821da9121b). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/c9e9ea8b9be2464cacd00b9c2a438e821da9121b...master) since then.\n* This project is partially sponsored by [Recall Masters](https://github.com/Recall-Masters) - look out for issues with `sponsored` tag.\n",
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-platonic/platonic-sqs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
