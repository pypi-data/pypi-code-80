# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['angelsaechsisch_telegram']

package_data = \
{'': ['*'],
 'angelsaechsisch_telegram': ['data/antworten.txt',
                              'data/antworten.txt',
                              'data/antworten.txt',
                              'data/antworten.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/ausnahmen.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/de.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt',
                              'data/google-10000-english.txt']}

install_requires = \
['python-telegram-bot>=13.4.1,<14.0.0']

setup_kwargs = {
    'name': 'angelsaechsisch-telegram',
    'version': '0.1.0',
    'description': "Ein wundervoller Telegram Roboter, der dich höflich daran erinnert kein Angelsächsisch zu nutzen. Nach dem Vorbild des besten Unter's dieser Erde: r/ich_iel",
    'long_description': None,
    'author': 'leuchtum',
    'author_email': 'acct.d-mueller@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
