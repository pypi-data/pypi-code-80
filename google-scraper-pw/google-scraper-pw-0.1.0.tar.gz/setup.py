# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_scraper_pw']

package_data = \
{'': ['*']}

install_requires = \
['get-pwbrowser>=0.1.1,<0.2.0',
 'linetimer>=0.1.4,<0.2.0',
 'logzero>=1.6.3,<2.0.0',
 'playwright>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'google-scraper-pw',
    'version': '0.1.0',
    'description': 'scrape google via playwright',
    'long_description': '# google-scraper-pw\n[![tests](https://github.com/ffreemt/google-scraper-playwright/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/google-scraper-pw.svg)](https://badge.fury.io/py/google-scraper-pw)\n\nscrape google using playwright, cross platform (Windows/MacOS/Linux)\n\n## Installation\n\n```bash\npip install google-scraper-pw\n# pip install google-scraper-pw -U  # upgrade to the latest version\npython -m playwright install chromium\n```\n<details>\n<summary>or via poetry</summary>\n<code style="white-space:wrap;">\npoetry add google-scraper-pw &&\npython -m playwright install chromium\n</code>\n</details>\n\nor\n```bash\npip install git+https://github.com/ffreemt/google-scraper-playwright.git\npython -m playwright install chromium\n```\n\nor clone the repo (``git clone https://github.com/ffreemt/google-scraper-playwright.git``) and install from it and\n```\npython -m playwright install chromium\n```\n\n## Usage\n\n```python\nfrom pprint import pprint\nfrom google_scraper_pw import google_tr\n\nres = google_tr("test me")\nprint(res)\n# \'考验我\'  # took 2.8s\n\n# google_tr preserves format\npprint(google_tr("test you\\n\\n test me", to_lang="de"))\n#\'teste dich\\n\\n  teste mich\'\n\ntext = "Playwright is a Python library to automate Chromium, Firefox and WebKit browsers with a single API. Playwright delivers automation that is ever-green, capable, reliable and fast. "\n\nprint(google_tr(text, to_lang="de"))\n\n# Playwright ist eine Python-Bibliothek, um Chrom-, Firefox- und Webkit-Browser mit einer einzigen API zu automatisieren. Der Dramatiker liefert Automatisierung, die jemals grün, fähig, zuverlässig und schnell ist.  # took: 2.5s\n```\n\n<!---\n\nIn [367]: doc0("div.lmt__textarea.lmt__textarea_dummydiv").text()\nOut[367]: \'test you are me new lines 试探你是我 新行\'\n\n# doc0("div#target-dummydiv").text()\nIn [371]: doc0("#target-dummydiv").text()\nOut[371]: \'试探你是我 新行\'\n\nIn [394]: doc0("#target-dummydiv").html()\nOut[394]: \'试探你是我\\n新行\\n\\n\'\n\n# doc0("button.lmt__translations_as_text__text_btn").text()\nIn [369]: doc0(".lmt__translations_as_text__text_btn").text()\nOut[369]: \'试探你是我 新行\'\nIn [369]: doc0(".lmt__translations_as_text__text_btn").html()\n\n\nIn [388]: re.findall(r"<button class=\\"lmt__translations_as_text__text_btn[\\s\\S]*?>[\\s\\S]*?<\\/button>", text0)\nOut[388]: [\'<button class="lmt__translations_as_text__text_btn">试探你是我\\n新行</button>\']\n\nre.findall(r"<div id=\\"target-dummydiv[\\s\\S]*?>[\\s\\S]*?<\\/div>", text0)\n[\'<div id="target-dummydiv" class="lmt__textarea lmt__textarea_dummydiv">试探你是我\\n新行\\n\\n</div>\']\n\n--->',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/google-scraper-playwright',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
