# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telewater']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'Telethon>=1.21.1,<2.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptg>=0.2.post2,<0.3',
 'hachoir>=3.1.2,<4.0.0',
 'python-dotenv>=0.16.0,<0.17.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['telewater = telewater.cli:app']}

setup_kwargs = {
    'name': 'telewater',
    'version': '0.0.4',
    'description': 'A telegram bot that applies watermark on images, gifs and videos.',
    'long_description': '# telewater\n\nA telegram bot that applies watermark on images, gifs and videos.\n\n\n## Requirements\n\nMake sure to have these installed in your system.\n\n- [python3.9+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) (the bot is built with the telethon library)\n- [ffmpeg](https://ffmpeg.org/) (used by the bot for applying watermark)\n\n### Verification\n\nOpen you terminal to check if you have all basic requirements properly installed.\n\n1. Run `python --version` and you should get something like this `Python 3.9.2` (or above).\n2. Run `pip --version` and you should get `pip 20.2.2` (or above).\n\n    > Some systems may require to use `python3` and `pip3` instead of the above.\n\n3. Run `ffmpeg -h` and it should display a help message and version above `4.2.4`.\n\n## Installation\n\n```shell\npip install telewater\n```\n\n\n## Configuration\n\nCreate a file named `.env` inside your current directory (or the directory from which you desire to run the `telewater` command.)\n\nFill the file with your `API_ID` and `API_HASH`\n\nExample:\n\n```txt\nAPI_ID=12345\nAPI_HASH=102837:kjfjfk9r9JOIJOIjoi_jf9wr0w\n```\n\nReplace the above values with the actual values. Learn [how to get them](https://docs.telethon.dev/en/latest/basic/signing-in.html) for your telegram account.\n\n\n## Usage\n\nTelewater has a simple command line interface to start the bot.\n\nSimply open your terminal and run `telewater`.\n\n\n> **Note:**\n> - It will prompt you to input the bot name and token.\n\nFor more advanced options, run `telewater --help`.\n\n```shell\nUsage: telewater [OPTIONS]\n\n  Run the bot with the username and token obtained from @BotFather.\n\nOptions:\n  -n, --name TEXT   Name of the bot you are runnning.  [env var: BOT_USERNAME;\n                    required]\n\n  -t, --token TEXT  Bot Token obtained from @BotFather.  [env var: BOT_TOKEN;\n                    required]\n\n  -l, --loud        Increase output verbosity.  [env var: LOUD]\n  -v, --version     Show version and exit.\n  --help            Show this message and exit.\n```\n\n\n\n> **Note:**\n> - In the above help text, you see `env var` specified for some options. The value of those options can be set by using an environment variable (of the specified name), instead of passing as a command line argument.\n> - You can write your enviroment variables for telewater inside a file called `.env` which lies in the same directory from which `telewater` command is invoked.\n\nFor any furthur help feel free to create an issue.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
