# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasett']

package_data = \
{'': ['*']}

install_requires = \
['dask==2021.3.1',
 'gcsfs==0.7.2',
 'google-api-core==1.26.3',
 'google-auth-oauthlib==0.4.4',
 'google-auth==1.28.0',
 'google-cloud-bigquery==2.13.1',
 'google-cloud-core==1.6.0',
 'google-cloud-datacatalog==3.1.1',
 'google-cloud-datastore==2.1.0',
 'google-cloud==0.34.0',
 'numpy==1.20.2',
 'pandas==1.2.3',
 'pyarrow>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'datasett',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'pbencze',
    'author_email': 'paul@idelab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.9.2',
}


setup(**setup_kwargs)
