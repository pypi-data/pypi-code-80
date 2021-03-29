# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_zebrunner', 'pytest_zebrunner.api']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.16.1,<0.17.0',
 'pydantic>=1.7.2,<2.0.0',
 'pytest>=6.1.1,<7.0.0',
 'python-dotenv>=0.15.0,<0.16.0']

entry_points = \
{'pytest11': ['pytest-zebrunner = pytest_zebrunner.plugin']}

setup_kwargs = {
    'name': 'pytest-zebrunner',
    'version': '0.1.0',
    'description': 'Pytest connector for Zebrunner reporting',
    'long_description': '# Zebrunner PyTest agent\n\n\nThe official Zebrunner Pytest agent provides reporting functionality. It can automatically track selenium sessions\nand send info about session details to Zebrunner backend. It can be ease integrated in project just by installing library\nand adding configuration file.\n\n\n## Installation\n---------------\n\n    pip install pytest-zebrunner\n\n## Configuration\n----------------\nLibrary don\'t ready for usage just after installation. It won\'t send data to\nzebrunner service without additional configuration. To configure app you need to\nspecify environment variables. It can be done by specifying variables in `.env`\nfile.\n\n<!-- groups:start -->\n### Environment variables\n```dosini\nSERVICE_URL=<zebrunner url>\nACCESS_TOKEN=<access_token>\nZEBRUNNER_PROJECT=ProjectName\nZEBRUNNER_ENABLED=true\nBUILD=1.25.16\nENV=stage\n```\n\nYou can configure agent only with environment variables. Another formats would\nbe added in future. Planed formats are `yaml`, `ini` and program arguments.\n\n- `SERVICE_URL` - [required] Base URL of Zebrunner service.\n\n- `ACCESS_TOKEN` - [required] Authorization token. You can find it in Account & profile section.\n\n- `ZEBRUNNER_PROJECT` - [required] Name of project.\n\n- `REPORTING_ENABLED` - You can disable agent if it makes side effects in you project or doesn\'t work.\n\n- `BUILD` - Version of product on which tests are running.\n\n- `ENV` - Testing environment name.\n<!-- groups:end -->\n\nIf required configurations not provided there is a warning in logs with problem description and names of options,\nwhich need to be specified. Parameter names are case insensitive and can be written in upper and lower registers.\n\n## Additional functionality\n---------------------------\n**IMPORTANT**: All attachments to tests can be done only while some test is running. All attachments to test-run can be done only while pytest test-session is active.\n---------------------------\n\n\n### Attach screenshot\n```python\nfrom pytest_zebrunner.attachments import attach_test_screenshot\n\n\ndef test_something():\n    ...\n    attach_test_screenshot("path_to_screenshot.png")\n    ...\n```\n\n### Attach artifact to test\n```python\nfrom pytest_zebrunner.attachments import attach_test_artifact\n\n\ndef test_something():\n    ...\n    attach_test_artifact("path_to_artifact")\n    ...\n```\n\n### Attach artifact-reference to test\n```python\nfrom pytest_zebrunner.attachments import attach_test_artifact_reference\n\n\ndef test_something():\n    ...\n    attach_test_artifact_reference("name", "reference")\n    ...\n```\n\n### Attach artifact to test-run\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_artifact\n\n\nattach_test_run_artifact("path_to_artifact")\n```\n\n### Attach artifact-reference to test-run\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_artifact_reference\n\n\nattach_test_run_artifact_reference("name", "reference")\n```\n\n### Attach labels to test\n```python\n@pytest.mark.label("name", "value")\ndef test_something():\n    ...\n```\nor\n```python\nfrom pytest_zebrunner.attachments import attach_test_label\n\n\ndef test_something():\n    ...\n    attach_test_label("name", "value")\n    ...\n```\n**Note:** These two methods can be combined.\n\n### Attach label to test run\n```python\nfrom pytest_zebrunner.attachments import attach_test_run_label\n\nattach_test_run_label("name", "value")\n```\n\n### Add maintainer to test\n```python\n@pytest.mark.maintainer("username_of_maintainer")\ndef test_something():\n    ...\n```\n',
    'author': 'Anatoliy Platonov',
    'author_email': 'p4m.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zebrunner.com/documentation/agents/pytest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
