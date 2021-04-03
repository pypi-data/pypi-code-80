# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_avro']

package_data = \
{'': ['*']}

install_requires = \
['fastavro>=1.3.4,<2.0.0',
 'singer-python>=5,<6',
 'smart_open>=5.0.0,<6.0.0',
 'strict_rfc3339>=0.7,<0.8']

entry_points = \
{'console_scripts': ['fmt = scripts:fmt',
                     'lint = scripts:lint',
                     'target-avro = target_avro:main',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'target-avro',
    'version': '0.2.0',
    'description': 'Singer.io target for extracting data',
    'long_description': '# target-avro\n\nThis is a [Singer](https://singer.io) target that reads JSON-formatted data\nfollowing the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).\n\n## Features\n\n- Output Avro files for [Singer](https://singer.io) streams\n- Output to cloud storages like Google Cloud Storage and Amazon S3, etc are supported powered by [smart_open](https://github.com/RaRe-Technologies/smart_open).\n\n## Install\n\n```sh\npip install target-avro\n```\n\n## Usage\n\n```sh\n# simple\ncat <<EOF | target-avro -c sample_config.json\n{"type":"STATE","value": {}}\n{"key_properties":["id"],"schema":{"properties":{"assignee":{"properties":{},"type":["null","object"]},"created_at":{"format":"date-time","type":["null","string"]},"id":{"type":["null","integer"]},"labels":{"items":{"properties":{"id":{"type":["null","integer"]},"name":{"type":["null","string"]}},"type":"object"},"type":["null","array"]},"locked":{"type":["null","boolean"]},"pull_request":{"properties":{"url":{"type":["null","string"]}},"type":["null","object"]},"title":{"type":"string"}},"selected":true,"type":["null","object"]},"stream":"issues","type":"SCHEMA"}\n{"type": "RECORD", "stream": "issues", "record": {"created_at":"2020-11-24T23:49:24.000000Z","id":12,"labels":[{"id":238,"name":"ABCDEFGHIJKLMNOPQRSTUV"}],"locked":true,"pull_request":{"url":"https://api.github.com/repos/sample/issues/pulls/999999"},"title":"ABCDEFGHIJKLMNOPQRSTUVWXY"}, "time_extracted": "2021-03-25T12:53:51.817781Z"}\n{"type": "STATE", "value": {"bookmarks": {"singer-io/singer-python": {"issues": {"since": "2020-11-24T23:49:24.000000Z"}}}}}\nEOF\n\n# complex\ncat ./tests/data/github.jsonl | target-avro -c sample_config.json\n```\n\n## Configuration\n\nThe fields available to be specified in the config file are specified\nhere.\n\n| Field | Type | Default | Details |\n| ---- | ---- | ---- | ---- |\n| `prefix` | `["string"]`  | `N/A` | The output uri prefix. See [smart_open](https://github.com/RaRe-Technologies/smart_open) for information about valid values and credentials. |\n| `disable_collection` | `["boolean", "null"]` | `false` | Include `true` in your config to disable [Singer Usage Logging](#usage-logging). |\n| `logging_level` | `["string", "null"]`  | `"INFO"` | The level for logging. Set to `DEBUG` to get things like HTTP requests executed, JSON and Avro schemas, etc. See [Python\'s Logger Levels](https://docs.python.org/3/library/logging.html#levels) for information about valid values. |\n\n## Known Limitations\n\n- Requires a [JSON Schema](https://json-schema.org/) for every stream.\n- Only string, string with date-time format, integer, number, boolean,\n  object, and array types with or without null are supported. Arrays can\n  have any of the other types listed, including objects as types within\n  items.\n    - Example of JSON Schema types that work\n        - `[\'number\']`\n        - `[\'string\']`\n        - `[\'string\', \'null\']`\n    - Exmaple of JSON Schema types that **DO NOT** work\n        - `[\'string\', \'integer\']`\n        - `[\'integer\', \'number\']`\n        - `[\'any\']`\n        - `[\'null\']`\n- JSON Schema combinations such as `anyOf` and `oneOf` are not supported.\n- JSON Schema `$ref` is not supported.\n\n## Usage Logging\n[Singer.io](https://www.singer.io/) requires official taps and targets to collect anonymous usage data. This data is only used in aggregate to report on individual tap/targets, as well as the Singer community at-large. IP addresses are recorded to detect unique tap/targets users but not shared with third-parties.\n\nTo disable anonymous data collection set disable_collection to true in the configuration JSON file.\n\n---\n\nCopyright &copy; 2021 Kageboushi\n',
    'author': 'inamura',
    'author_email': 'inamura@kageboushi.app',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kageboushi-app/target-avro',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
