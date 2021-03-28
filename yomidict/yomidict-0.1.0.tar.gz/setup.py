# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yomidict']

package_data = \
{'': ['*']}

install_requires = \
['fugashi>=1.1.0,<2.0.0', 'srt>=3.4.1,<4.0.0', 'unidic>=1.0.3,<2.0.0']

setup_kwargs = {
    'name': 'yomidict',
    'version': '0.1.0',
    'description': 'Create dictionaries for yomichan',
    'long_description': '# yomidict\ncreate dictionaries for yomichan\n\nMWE:\n```python\nimport yomidict\ndm = yomidict.DictMaker()\nfilelist = ["test.html" for _ in range(5)]\ndm.feed_files(filelist)\ndm.save("zipfile.zip", "name_in_yomichan")\n```',
    'author': 'exc4l',
    'author_email': 'cps0537@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/exc4l/yomidict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
