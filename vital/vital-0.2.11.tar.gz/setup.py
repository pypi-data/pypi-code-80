# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vital', 'vital.api', 'vital.internal']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.0.1,<3.0.0',
 'arrow',
 'auth0-python',
 'importlib-metadata>=3.7.3,<4.0.0',
 'requests']

setup_kwargs = {
    'name': 'vital',
    'version': '0.2.11',
    'description': '',
    'long_description': '# vital-python\n\nThe official Python Library for [Vital API](https://docs.tryvital.io)\n\n\n# Install\n```\npip install vital\n```\n\n# Calling Endpoints\n\n```\nfrom vital import Client\n\n# Available environments are \'sandbox\', \'development\', and \'production\'.\nclient = Client(client_id=\'***\', secret=\'***\', environment=\'sandbox\')\n```\n\n# Supported Endpoints\n\n```\nclient.LinkToken.create(user_key="user_key")\nclient.Body.get(user_key=**,start_date="2020-01-01", end_date="2020-10-10")\nclient.Activity.get(user_key=**,start_date="2020-01-01", end_date="2020-10-10")\nclient.Sleep.get(user_key=**,start_date="2020-01-01", end_date="2020-10-10")\nclient.SourceSpecific.get(user_key=**,start_date="2020-01-01", end_date="2020-10-10")\nclient.User.create(client_user_id=**)\nclient.User.providers(user_key=**)\n```\n',
    'author': 'maitham',
    'author_email': 'maitham@tryvital.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adeptlabs/vital-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
