# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mtg_parser']

package_data = \
{'': ['*']}

install_requires = \
['pyparsing>=2.4.7,<3.0.0']

setup_kwargs = {
    'name': 'mtg-parser',
    'version': '0.0.1a0',
    'description': '',
    'long_description': '# Quickstart\n\n\tmake install\n\tmake test\n\tmake build\n\tmake clean\n\nor\n\n\tmake\n\n# Publish a new version\n\n## Test\n\n\tpoetry version (premajor|preminor|prepatch|prerelease)\n\tmake test\n\tmake lint\n\tmake build\n\tmake test-publish\n\n## Publish\n\n\tpoetry version (major|minor|patch)\n\tmake build\n\tmake publish\n',
    'author': 'Ludovic Heyberger',
    'author_email': '940408+lheyberger@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
