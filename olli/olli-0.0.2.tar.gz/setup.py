# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olli']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.16.0,<0.17.0',
 'schedule>=1.0.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['olli = olli.__main__:start']}

setup_kwargs = {
    'name': 'olli',
    'version': '0.0.2',
    'description': 'Olli searches your Loki logs and relays matching terms to Discord.',
    'long_description': '# Olli\n\n[![PyPI version fury.io](https://badge.fury.io/py/olli.svg)](https://pypi.python.org/pypi/olli/)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/olli.svg)](https://pypi.python.org/pypi/olli/)\n[![GitHub license](https://img.shields.io/github/license/python-discord/olli.svg)](https://github.com/python-discord/olli/blob/main/LICENSE)\n\nOlli searches your Loki logs and relays matching terms to Discord. Please read the [documentation](https://python-discord.github.io/olli/) to get started.\n\n- [Documentation](https://python-discord.github.io/olli/)\n- [Docker Image](https://ghcr.io/python-discord/olli)\n\n## Contributing\n\nPlease open an issue before contributing features to discuss implementation.\n\n## License\n\nOlli is licensed under MIT.\n',
    'author': 'Joe Banks',
    'author_email': 'joseph@josephbanks.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://python-discord.github.io/olli/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
