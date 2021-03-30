# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_code_validator']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3,<4.0', 'mkdocs>=1.0,<2.0', 'pymdown-extensions>=8.0,<9.0']

entry_points = \
{'mkdocs.plugins': ['code-validator = '
                    'mkdocs_code_validator.plugin:CodeValidatorPlugin']}

setup_kwargs = {
    'name': 'mkdocs-code-validator',
    'version': '0.1.0',
    'description': 'Checks Markdown code blocks in a MkDocs site against user-defined actions',
    'long_description': None,
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oprypin/mkdocs-code-validator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
