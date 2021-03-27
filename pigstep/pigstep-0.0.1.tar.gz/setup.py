# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pigstep']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.18.0,<0.19.0', 'pynbs>=0.4.2,<0.5.0']

setup_kwargs = {
    'name': 'pigstep',
    'version': '0.0.1',
    'description': 'A beet plugin for importing songs into Minecraft',
    'long_description': "# pigstep\n\n[![GitHub Actions](https://github.com/vberlier/pigstep/workflows/CI/badge.svg)](https://github.com/vberlier/pigstep/actions)\n[![PyPI](https://img.shields.io/pypi/v/pigstep.svg)](https://pypi.org/project/pigstep/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pigstep.svg)](https://pypi.org/project/pigstep/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A beet plugin for importing songs into Minecraft.\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install pigstep\n```\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you're using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort pigstep tests\n$ poetry run black pigstep tests\n$ poetry run black --check pigstep tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/pigstep/blob/main/LICENSE)\n",
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/pigstep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
