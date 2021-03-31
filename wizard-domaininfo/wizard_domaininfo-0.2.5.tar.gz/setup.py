# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wizard_domaininfo']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=2.0.0,<3.0.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'contextvars>=2.4,<3.0',
 'immutables>=0.15,<0.16',
 'importlib-metadata>=3.7.0,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'typing>=3.7.4,<4.0.0',
 'zipp>=3.4.1,<4.0.0']

entry_points = \
{'console_scripts': ['pwhois = wizard_domaininfo:pwhois',
                     'wizard-domaininfo = wizard_domaininfo.cli:main']}

setup_kwargs = {
    'name': 'wizard-domaininfo',
    'version': '0.2.5',
    'description': 'DNS/Whois Domain Information library',
    'long_description': '# Wizard Domaininfo\n\n[![pipeline status](https://gitlab.com/mikeramsey/wizard-domaininfo/badges/master/pipeline.svg)](https://gitlab.com/mikeramsey/wizard-domaininfo/pipelines)\n[![coverage report](https://gitlab.com/mikeramsey/wizard-domaininfo/badges/master/coverage.svg)](https://gitlab.com/mikeramsey/wizard-domaininfo/commits/master)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mikeramsey.gitlab.io/wizard-domaininfo/)\n[![pypi version](https://img.shields.io/pypi/v/wizard-domaininfo.svg)](https://pypi.org/project/wizard-domaininfo/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/wizard-domaininfo/community)\n\nDNS/Whois Domain Information library\n\n## Requirements\n\nWizard Domaininfo requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install wizard_domaininfo\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 wizard_domaininfo\n```\n\n=========\n\nA WHOIS DNS retrieval and parsing library for Python.\n\n## Dependencies\n\nNone! All you need is the Python standard library. Optional RDAP WHOIS based lookups require requests and json libraries. Optional DNS lookups are based on aiodns library.\n\n## Instructions\n\nThe whois legacy manual HTML version is also viewable [here](http://cryto.net/pythonwhois).\nThe new manual for RDAP based whois and DNS is located [here](https://mikeramsey.gitlab.io/wizard-domaininfo/).\n## Goals\n\n* 100% coverage of WHOIS/DNS formats.\n* Accurate and complete data.\n* Consistently functional parsing; constant tests to ensure the parser isn\'t accidentally broken.\n\n## Features\n\n* WHOIS data retrieval\n\t* Able to follow WHOIS server redirects\n\t* Won\'t get stuck on multiple-result responses from verisign-grs\n* WHOIS data parsing\n\t* Base information (registrar, etc.)\n\t* Dates/times (registration, expiry, ...)\n\t* Full registrant information (!)\n\t* Nameservers\n* Optional WHOIS data normalization\n\t* Attempts to intelligently reformat WHOIS data for better (human) readability\n\t* Converts various abbreviation types to full locality names\n\t\t* Airport codes\n\t\t* Country names (2- and 3-letter ISO codes)\n\t\t* US states and territories\n\t\t* Canadian states and territories\n\t\t* Australian states\n* `pwhois`, a simple WHOIS tool using pythonwhois\n\t* Easily readable output format\n\t* Can also output raw WHOIS data\n\t* ... and JSON.\n* Automated testing suite for parse.py and legacy whois(non rdap based)\n\t* Will detect and warn about any changes in parsed data compared to previous runs\n\t* Guarantees that previously working WHOIS parsing doesn\'t unintentionally break when changing code\n* Automated testing suite for rdap and aiodns is based on pytest\n* Fast Asynchronous DNS lookups via c-ares aiodns library and helper methods in utils.py.\n* Single call via DomainInfo class in domaininfo.py will get all available DNS/Whois via rdap and fallback to legacy whois as needed.\n\t* Checks for WAFs(Cloudflare/Sucuri/Quic.Cloud)\n\t* Check domain expiration.\n\t* Check for or enumerate DKIM records and selectors.\n\t* Check Whois Nameservers and DNS nameservers match.\n\t* See [here](https://gitlab.com/mikeramsey/wizard-domaininfo/-/blob/master/src/wizard_domaininfo/domaininfo.py#L23-69) for all the class attributes.\n\t\n\n## Important update notes\n\n\n## It doesn\'t work!\n\n* It doesn\'t work at all?\n* It doesn\'t parse the data for a particular domain?\n* There\'s an inaccuracy in parsing the data for a domain, even just a small one?\n\nIf any of those apply, don\'t hesitate to file an issue! The goal is 100% coverage, and we need your feedback to reach that goal.\n\n## License\n\nThis library may be used under the MIT License.\n\n## Data sources\n\nThis library uses a number of third-party datasets for normalization:\n\n* `airports.dat`: [OpenFlights Airports Database](http://openflights.org/data.html) ([Open Database License 1.0](http://opendatacommons.org/licenses/odbl/1.0/), [Database Contents License 1.0](http://opendatacommons.org/licenses/dbcl/1.0/))\n* `countries.dat`: [Country List](https://github.com/umpirsky/country-list) (MIT license)\n* `countries3.dat`: [ISO countries list](https://gist.github.com/eparreno/205900) (license unspecified)\n* `states_au.dat`: Part of `pythonwhois` (WTFPL/CC0)\n* `states_us.dat`: [State Table](http://statetable.com/) (license unspecified, free reuse encouraged)\n* `states_ca.dat`: [State Table](http://statetable.com/) (license unspecified, free reuse encouraged)\n\nBe aware that the OpenFlights database in particular has potential licensing consequences; if you do not wish to be bound by these potential consequences, you may simply delete the `airports.dat` file from your distribution. `pythonwhois` will assume there is no database available, and will not perform airport code conversion (but still function correctly otherwise). This also applies to other included datasets.\n\n## Contributing\n\nFeel free to fork and submit pull requests (to the `develop` branch)! If you change any parsing or normalization logic, ensure to run the full test suite before opening a pull request. Instructions for that are below.\n\nPlease note that this project uses tabs for indentation.\n\nAll commands are relative to the root directory of the repository.\n\n**Pull requests that do _not_ include output from test_parse.py will be rejected!**\n\n### Adding new WHOIS data to the testing set\n\n\tpwhois --raw thedomain.com > test/data/thedomain.com\n\t\n### Checking the currently parsed data (while editing the parser)\n\n\t./pwhois -f test/data/thedomain.com/ .\n\t\n(don\'t forget the dot at the end!)\n\t\n### Marking the current parsed data as correct for a domain\n\nMake sure to verify (using `pwhois` or otherwise) that the WHOIS data for the domain is being parsed correctly, before marking it as correct!\n\n\tpython test_parse.py update thedomain.com\n\t\n### Running all tests\n\n\tpython test_parse.py run all\n\t\n### Testing a specific domain\n\n\tpython test_parse.py run thedomain.com',
    'author': 'Michael Ramsey',
    'author_email': 'mike@hackerdise.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mikeramsey/wizard-domaininfo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
