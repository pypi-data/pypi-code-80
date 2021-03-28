# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plucker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'plucker',
    'version': '0.1.0',
    'description': 'Validate and extract JSON-sourced data into type-safe dataclasses',
    'long_description': '# `plucker`\n\n[![Build Status](https://github.com/takkaria/plucker/workflows/test/badge.svg?branch=master&event=push)](https://github.com/takkaria/plucker/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/takkaria/plucker/branch/master/graph/badge.svg)](https://codecov.io/gh/takkaria/plucker)\n[![Python Version](https://img.shields.io/pypi/pyversions/plucker.svg)](https://pypi.org/project/plucker/)\n\nValidate and extract JSON-sourced data into type-safe dataclasses\n\n\n## wut\n\n* Tired of relying on vendor-provided, untyped Python libraries to interface with external APIs?\n* Want to just make a few simple HTTP requests without the weight of extra dependencies?\n* Do you only use a small subset of the data you get from external sources, picking out five fields when you are given thirty?\n* Are you more than slightly worried that the API might change under you and you wouldn\'t know?\n* Want to avoid just reaching into dictionaries to get the data you want?\n* Do you want to parse the JSON you get into something type-safe so that mypy will complain when you do wrong things?\n* Is writing fakes a bit too heavyweight for the APIs you\'re calling?  Would producing an error on unexpected input work OK for now?\n\nEnter `plucker`.\n\n`plucker` is designed to validate, map and reduce regularly structured data into `dataclass`es.  That data would typically be JSON from APIs but could be anything that mostly consists of Python dicts and lists when parsed.\n\n`plucker` will either give you type-verified data, or it will fail with helpful error messages:\n\n```\nData not in expected format; expected fred to be \'list\' but it was \'dict\':\n.fred[].v\n ^^^^\n```\n\nJust pick the data you want using `jq`-style paths, map it so that it\'s the right type if you need to, and you have well-typed validated data to feed into the rest of your system.\n\n\n## Installation (soon...)\n\n```bash\npip install plucker\n```\n\n\n## Example\n\n\n\n```python\nfrom typing import List\nfrom dataclasses import dataclass\nfrom enum import Enum, auto\nfrom datetime import date\n\nfrom plucker import pluck, Path\n\n\nclass Status(Enum):\n    """A cintact\'s status."""\n    CURRENT = auto()\n    EXPIRED = auto()\n\n\n@dataclass\nclass Contact:\n    """A contact record."""\n    name: str\n    email: str\n\n\n@dataclass\nclass Struct:\n    """The typed dataclass we want our data collected into."""\n    date: date\n    id: int\n    state: Status\n    affected_records: List[int]\n    contacts: List[Contact]\n\n\nTO_STATUS = {"CUR": Status.CURRENT, "EXP": Status.EXPIRED}\n\ninput_ = {\n    "date": "2021-01-01",\n    "id": "1242",\n    "payload": {\n        "from": "CURRENT",\n        "who": [\n            {"name": "DM", "id": 1, "email": "dangermouse@example.com"},\n            {"name": "Stiletto", "id": 23, "email": "baroni@example.com"},\n        ]\n    }\n}\n\nplucked = pluck(\n    input_,\n    Struct,\n    date=Path(".date"),\n    id=Path(".id").map(int),\n    state=Path(".payload.from").map(TO_STATUS),\n    affected_records=Path(".payload.who[].id"),\n    people=Path(".payload.who[]").into(\n        Contact,\n        name=Path(".name"),\n        email=Path(".email"),\n    ),\n)\n\nexpected = Struct(\n    date=date(2021, 1, 1),\n    id=1242,\n    state=Status.CURRENT,\n    affected_records=[1, 23],\n    contacts=[\n        Contact("DM", "dangermouse@example.com"),\n        Contact("Stiletto", "baroni@example.com")\n    ]\n)\n\nassert plucked == expected\n# ^ it\'s True\n```\n\n\n## Prior art\n\n1. dataclasses_json -> require the same structure between JSON and serialization, which means you have to specify an intermediate structure\n2. DRF serializers -> heavyweight and not type safe, destructure into dictionaries\n3. Elm\'s JSON decoders -> this design isn\'t really based on anything in there but ever since using them I wanted similar functionality in Python\n4. `jq`, an amazing commandline tool for querying JSON data\n5. [Parse, don\'t validate](https://lexi-lambda.github.io/tags/functional-programming.html)\n6. Elm\'s error messages\n\n\n## License\n\n[MIT](https://github.com/takkaria/plucker/blob/master/LICENSE)\n\n\n## Credits\n\nA bunch of the tooling was taken from [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package) but then heavily modified.\n',
    'author': 'Anna Sidwell',
    'author_email': 'anna@takkaria.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/takkaria/plucker',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
