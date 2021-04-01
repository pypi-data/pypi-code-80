# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sweetcurves', 'sweetcurves.catelog']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'decorator>=4.4.2,<5.0.0',
 'devtools>=0.6.1,<0.7.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.1,<2.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'sh>=1.14.1,<2.0.0',
 'toolz>=0.11.0,<0.12.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['sweets = sweetcurves.main:app']}

setup_kwargs = {
    'name': 'sweetcurves',
    'version': '0.1.5',
    'description': 'Slight build automation and changes.',
    'long_description': '# SweetCurves\n\nThis mini project is only to take the current repo and modify it to match the parameters for kaniko.\n\n\n<!-- gcloud iam service-accounts keys create super-cloud-key.json --iam-account=full-access@astute-impulse-303109.iam.gserviceaccount.com -->',
    'author': 'Kevin Hill',
    'author_email': 'kah.kevin.hill@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
