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
    'version': '0.1.1',
    'description': 'Memrise audio uploader',
    'long_description': '# Memrise audio uploader\n\nA command-line tool to upload text-to-speech audio to Memrise courses. Audio is generated using Google Text-to-Speech synthesizator.\n\n## Usage\n\nYou can input your Memrise credentials when prompted in the command line or alternatively you can define them in a dotenv file. Save `MEMRISE_USERNAME` and/or `MEMRISE_PASSWORD` to a `.env` file in your current folder.\n\nYou will need access to a Google Cloud project with Google Cloud Text to Speech API enabled. The application uses default credentials for accessing Google Cloud. For more information, see:\n\n- [Getting started with Cloud SDK](https://cloud.google.com/sdk)\n- [Cloud SDK Application Default Credentials](https://cloud.google.com/sdk/gcloud/reference/auth/application-default)\n- [Cloud Text-to-Speech - Quickstart](https://cloud.google.com/text-to-speech/docs/quickstart-protocol)\n',
    'author': 'Olli Paakkunainen',
    'author_email': 'olli@paakkunainen.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ollipa/memrise-audio-uploader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
