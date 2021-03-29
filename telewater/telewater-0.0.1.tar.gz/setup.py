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
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['poetry = telewater.cli:main']}

setup_kwargs = {
    'name': 'telewater',
    'version': '0.0.1',
    'description': 'A telegram bot that applies watermark on images, gifs and videos.',
    'long_description': '# watermark-gif-bot\n\nA telegram bot that helps you apply an watermark image on GIFs.\n\n**The following instructions assume that the reader is comfortable with the following tasks**\n\n- using the terminal,\n- cloning repositories using `git`,\n- running `python` programs, and\n- using bots/userbots made with the [Telethon](https://github.com/LonamiWebs/Telethon) library.\n\n\n## Requirements\n\n- [python3.9+](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installing/) (the bot is built with the telethon library)\n- [ffmpeg](https://ffmpeg.org/) (used by the bot for applying watermark)\n- [git](https://git-scm.com/) (for installing and updating this repo on your server)\n\n\n## Installation\n\n```shell\n\ngit clone https://github.com/aahniks/watermarker.git\ncd watermarker\n\n```\n\n\n## Configuration\n\nCreate a file named `.env` inside the `watermarker` directory.\n\nFill the file with your `API_ID` and `API_HASH`\n\nExample:\n\n```txt\nAPI_ID=12345\nAPI_HASH=102837:kjfjfk9r9JOIJOIjoi_jf9wr0w\n```\n\nReplace the above values with the actual values. Learn [how to get them](https://docs.telethon.dev/en/latest/basic/signing-in.html) for your telegram account.\n\n\n## Run\n\nThe `main.py` file is the entry point for running the bot. Run this module using the correct python version.\n',
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
