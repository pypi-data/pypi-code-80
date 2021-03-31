# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dicomtrolley']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'pydicom>=2.1.2,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'dicomtrolley',
    'version': '0.2.0',
    'description': 'Retrieve medical images via DICOM-QR and DICOMweb',
    'long_description': None,
    'author': 'sjoerdk',
    'author_email': 'sjoerd.kerkstra@radboudumc.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
