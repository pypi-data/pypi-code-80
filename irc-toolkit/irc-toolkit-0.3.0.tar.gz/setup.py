# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['irctk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'irc-toolkit',
    'version': '0.3.0',
    'description': 'A Python IRCv3 Client Library',
    'long_description': "irc-toolkit\n===========\n\n[![Build Status](http://img.shields.io/travis/kylef/irctk/master.svg?style=flat)](https://travis-ci.org/kylef/irctk)\n[![Test Coverage](http://img.shields.io/coveralls/kylef/irctk/master.svg?style=flat)](https://coveralls.io/r/kylef/irctk)\n\nAn IRC client toolkit in Python.\n\n## Installation\n\n```bash\n$ pip install irc-toolkit\n```\n\n## Usage\n\n```python\nimport asyncio\nimport irctk\n\n\nclass Bot:\n    async def connect(self, hostname, port=6697, secure=True):\n        client = irctk.Client()\n        client.delegate = self\n        await client.connect(hostname, port, secure)\n\n    def irc_registered(self, client):\n        channel = client.add_channel('#test')\n        channel.join()\n\n    def irc_private_message(self, client, nick, message):\n        if message == 'ping':\n            nick.send('pong')\n\n    def irc_channel_message(self, client, nick, channel, message):\n        if message == 'ping':\n            channel.send('{}: pong'.format(nick))\n\n\nif __name__ == '__main__':\n    bot = Bot()\n\n    loop = asyncio.get_event_loop()\n    loop.create_task(bot.connect('chat.freenode.net'))\n    loop.run_forever()\n```\n\n",
    'author': 'Kyle Fuller',
    'author_email': 'kyle@fuller.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
