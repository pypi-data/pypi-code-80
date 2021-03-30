# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ment']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['m = ment.main:main']}

setup_kwargs = {
    'name': 'ment',
    'version': '0.1.4',
    'description': 'python library to write daily log in markdown quickly and to synthesize daily logs based on category',
    'long_description': '# ment\n## what is this?\nment is a python library to write daily log in markdown quickly and to synthesize daily logs based on category.\n\n## prerequisities\n- vim\n\n## how to install and run ment\n```\npip install ment\nm # start editting ~/ment_dir/<todays_date>/diary.md\n```\n\n## structure\n```\n~/ment_dir/\n├── 2021-03-27\n│\xa0\xa0 └── diary.md\n├── 2021-03-28\n│\xa0\xa0 └── diary.md\n├── 2021-03-29\n│\xa0\xa0 └── diary.md\n├── 2021-03-30\n│\xa0\xa0 └── diary.md\n└── synthe\n    ├── tag1\n    │\xa0\xa0 └── synthe_tag1.md\n    ├── tag2\n    │\xa0\xa0 └── synthe_tag2.md\n    ├── tag3\n    │\xa0\xa0 └── synthe_tag3.md\n    └── weeks.md\n\n```\n',
    'author': 'kawagh',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kawagh/ment',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
