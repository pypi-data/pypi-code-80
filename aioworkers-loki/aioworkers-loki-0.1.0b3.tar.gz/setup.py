# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioworkers_loki']

package_data = \
{'': ['*']}

install_requires = \
['aioworkers>=0.18,<0.19', 'python-logging-loki>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'aioworkers-loki',
    'version': '0.1.0b3',
    'description': '',
    'long_description': 'aioworkers-loki\n===============\n\n.. image:: https://img.shields.io/pypi/v/aioworkers-loki.svg\n  :target: https://pypi.org/project/aioworkers-loki\n  :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/aioworkers-loki.svg\n  :target: https://pypi.org/project/aioworkers-loki\n  :alt: Python versions\n\nAbout\n=====\n\nIntegration with `grafana loki <https://grafana.com/docs/loki/latest/>`_.\nWorks on `python-logging-loki <https://pypi.org/project/python-logging-loki>`_\n\nUse\n---\n\n.. code-block:: yaml\n\n    logging:\n      version: 1\n      root:\n        handlers: [loki]\n      handlers:\n        loki:\n          host: localhost:3100\n\n\nDevelopment\n-----------\n\nInstall dev requirements:\n\n\n.. code-block:: shell\n\n    poetry install\n\n\nRun linters:\n\n.. code-block:: shell\n\n    make\n',
    'author': 'Alexander Malev',
    'author_email': 'malev@somedev.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aioworkers/aioworkers-loki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
