# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['connect',
 'connect.telegram_bot',
 'connect.telegram_bot.decorators',
 'connect.telegram_bot.errors',
 'connect.telegram_bot.renderers']

package_data = \
{'': ['*']}

install_requires = \
['django==2.2.19', 'python-telegram-bot>=13.3,<14.0']

setup_kwargs = {
    'name': 'connect-telegram-bot',
    'version': '1.0.1',
    'description': 'Connect Telegram Bot',
    'long_description': "# Connect Telegram Bot\n\n![pyversions](https://img.shields.io/pypi/pyversions/connect-telegram-bot.svg) [![PyPi Status](https://img.shields.io/pypi/v/connect-telegram-bot.svg)](https://pypi.org/project/connect-telegram-bot/) [![Build Connect Telegram Bot](https://github.com/cloudblue/connect-telegram-bot/actions/workflows/build.yml/badge.svg)](https://github.com/cloudblue/connect-telegram-bot/actions/workflows/build.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=connect-telegram-bot&metric=alert_status)](https://sonarcloud.io/dashboard?id=connect-telegram-bot) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=connect-telegram-bot&metric=coverage)](https://sonarcloud.io/dashboard?id=connect-telegram-bot) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=connect-telegram-bot&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=connect-telegram-bot)\n\n## Introduction\n\n`Connect Telegram Bot` is the base class which helps to build custom commands for the django models. It allows getting historical data from django models, as well as develop custom pre-defined filters and execute custom django management commands (i.e. those which are executed through  `python manage.py $command`)\n\n## Install\n\n`Connect Telegram Bot` requires python 3.8 or later and has the following dependencies:\n\n* python-telegram-bot >=13.3\n* django>=2.2.19\n\n`Connect Telegram Bot` can be installed from [pypi.org](https://pypi.org/project/connect-telegram-bot/) using pip:\n\n```\n$ pip install connect-telegram-bot\n```\n\n## Running The Bot\n### Define your command class extending the base\n\nFor example:\n\n``` \n\nfrom myapp.models import MyAppModel\n\nfrom telegram_bot.telegram_conversation import TelegramConversation\n\n\nclass MyAppConversation(TelegramConversation):\n    COMMANDS_DIR = '/app/myapp/management/commands'\n\n    def __init__(self, logger, suffix):\n        super().__init__(logger, suffix)\n        self.model = MyAppModel\n\n    @property\n    def saved_filters(self):\n        return [\n            'count',\n        ]\n\n    def get_count(self, update):\n        amount = self._get_initial_queryset().count()\n        self._reply(update, amount)\n        self._default_query_context()\n\n\n```\n\nCreate a directory in your project where these conversation implementations will be placed.\n`Connect Telegram Bot` requires multiple environment variables to be setup before executing:\n\n| Variable      | Description  |\n| ------------- |:-------------|\n|`TELEGRAM_BOT_TOKEN`|Telegram Token for the bot. Please refer to https://core.telegram.org/bots on how to create a bot.|\n|`DJANGO_SETTINGS_MODULE`|Django settings package for current project.|\n|`TELEGRAM_BOT_HANDLERS`|Directory where custom conversations (handlers) were placed, i.e. where we would put our `MyAppConversation` from above|\n|`TELEGRAM_BOT_COMMAND_SUFFIX`|In case of having multiple instances of the bot (with the same commands) we want to add some suffix to the commands, so that only specific bot is getting the command, so command becomes `myappconversation_${SUFFIX}`. If there is no need to have multiple instances of the same bot in the chat -- just leave this undefined. |\n\n### Running The Bot\n\n`export TELEGRAM_BOT_TOKEN='....'; export DJANGO_SETTINGS_MODULE='settings.common'; export TELEGRAM_BOT_HANDLERS='/app/telegram_bot/conversation_handlers/'; export TELEGRAM_BOT_COMMAND_SUFFIX='suf1'; python telegram_bot/bot.py`\n\n## Testing\n\n* Create virtualenv\n* Install project dependencies\n```commandline\npython -m pip install --upgrade pip\npip install poetry\npoetry update\n```\n* Run tests\n```commandline\npoetry run pytest\n```\n\n\n## License\n\n``Connect Telegram Bot`` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).",
    'author': 'CloudBlue LLC',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://connect.cloudblue.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
