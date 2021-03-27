# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memrise_audio_uploader',
 'memrise_audio_uploader.lib',
 'memrise_audio_uploader.lib.memrise']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-texttospeech>=2.2.0,<3.0.0',
 'lxml>=4.6.3,<5.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'memrise-audio-uploader',
    'version': '0.1.0',
    'description': 'Memrise audio uploader',
    'long_description': None,
    'author': 'Olli Paakkunainen',
    'author_email': 'olli@paakkunainen.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
