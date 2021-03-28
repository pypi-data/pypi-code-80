# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypeme']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hypeme',
    'version': '0.1.3',
    'description': 'hype yourself up!',
    'long_description': '# hypeme\nhype yourself up!\n\n## Installation\n\n```\npip install hypeme\n```\n\n## Usage\n\ntired of ur boring old print statement?\n\n```python\n>>> print(\'yeah\')\nyeah :(\n```\n\nas we like to say, hype yourself up!\n\n```python\n>>> import hypeme\n>>> print(\'how?\')\nHOW?!!!!!!!\n>>> print(\'oh wow i am a good and caring person\')\nOH WOW I AM A GOOD AND CARING PERSON!!\n```\n\nshould work on most stuff!!\n\n```python\n>>> import numpy as np\n>>> print(np.zeros((3,3)))\nARRAY([[0., 0., 0.],\n       [0., 0., 0.],\n       [0., 0., 0.]])!!!!!!!!!\n>>> print(np.array)\n<BUILT-IN FUNCTION ARRAY>!!!!!!!!!!\n>>> print([1, 2, 3, \'birds\', set(\'and\'), b\'bees\'])\n[1, 2, 3, \'BIRDS\', {\'A\', \'D\', \'N\'}, B\'BEES\']!!!!!!!!!\n```\n\nif it doesn\'t it\'s still nice about it\n\n```python\nclass NoRepr:\n    def __repr__(self):\n        raise Exception(\'You cant represent me!\')\n\n>>> print(NoRepr())\nIF I CANT YELL IT THEN I WONT PRINT IT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n>>> hypeme.relax()\nok sorry i just get excited for you is all\n\nTraceback (most recent call last):\n  File "<stdin>", line 1, in <module>\n  File "/Users/jonny/git/hypeme/hypeme/__init__.py", line 34, in relax\n    builtins.ye_olde_print(_LAST_PRINT)\n  File "<stdin>", line 3, in __repr__\nException: You cant represent me!\n```\n\nand when you are fully hyped you can go back to the real world\n```python\n>>> hypeme.no_hyping()\nsmell ya later!\n>>> print(\'so quiet in here all of a sudden\')\nso quiet in here all of a sudden\n```\n\n\n\n',
    'author': 'sneakers-the-rat',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakers-the-rat/hypeme/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.3',
}


setup(**setup_kwargs)
