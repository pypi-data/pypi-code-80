# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['random_standup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'tomlkit>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['standup = random_standup.standup:standup']}

setup_kwargs = {
    'name': 'random-standup',
    'version': '1.0.0',
    'description': 'Standup Randomizer',
    'long_description': '[![Build](https://github.com/jidicula/random-standup-py/actions/workflows/build.yml/badge.svg)](https://github.com/jidicula/random-standup-py/actions/workflows/build.yml) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![PyPI](https://img.shields.io/pypi/v/random-standup)](https://pypi.org/project/random-standup/)\n\n# 🎲random-standup-py🐍\nDo you have awkward pauses in your standups because no one wants to give their\nupdate next? Why not have a defined order? To make it fair, why not also\n🎲randomize🎲 that order!\n\nYou *really* should use [the Go version](https://pkg.go.dev/github.com/jidicula/random-standup) of this tool. This Python version was developed solely as a comparison exercise for the package publishing process.\n\n### Do you find this useful?\n\nStar this repo!\n\n### Do you find this *really* useful?\n\nYou can sponsor me [here](https://github.com/sponsors/jidicula)!\n\n## Usage\n\n1. Get the tool with `pip install random-standup`.\n\n2. Create a team roster in a TOML file, following the format in\n`example-roster.toml`:\n```toml\n[Subteam-1]\nmembers = [\n        "Alice",                # TOML spec allows whitespace to break arrays\n        "Bob",\n        "Carol",\n        "David"\n        ]\n\n["Subteam 2"]                   # Keys can have whitespace in quoted strings\nmembers = ["Erin", "Frank", "Grace", "Heidi"]\n```\n\n3. `standup example-roster.toml`\n\n## Output\n```\n$ standup example-roster.toml\n2021-03-25\n## Subteam-1\nAlice\nBob\nDavid\nCarol\n\n## Subteam 2\nErin\nGrace\nFrank\nHeidi\n```\n\n## Building from `main`\n\n1. Clone and `cd` into the repo.\n2. Install [Poetry](https://python-poetry.org/docs/#installation).\n3. `poetry install`\n4. `poetry run standup example-roster.toml`\n\nRun tests with `poetry run pytest -v`\n',
    'author': 'jidicula',
    'author_email': 'johanan@forcepush.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jidicula/random-standup-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
