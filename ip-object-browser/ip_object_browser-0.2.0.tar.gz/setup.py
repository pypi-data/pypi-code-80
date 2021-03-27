# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ip_object_browser']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=20.2.1,<21.0.0', 'ipython>=7.21.0,<8.0.0', 'urwid>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'ip-object-browser',
    'version': '0.2.0',
    'description': 'Browse big nested data structures in ipython with keyboard',
    'long_description': '# ip_object_browser\nUsing IPython? Did a REST endpoint return 5 MB of JSON data? Can\'t bother to save the response to a file?\nBrowse it with your keyboard straight from the console!\n\n## Usage\n\nIn IPython, press `<C-T>` to browse the last output object (`_`).\n\nUse vi-like `hjkl` or arrow keys to navigate. \n\nPress `<C-C>` or `q` to exit.\n\n### Usage from code\n```python\nfrom ip_object_browser import view\nview({})\n```\n\n## Installation\n```bash\npip install ip-object-browser\ncat <<EOF >>~/.ipython/profile_default/ipython_config.py\nc = get_config()\nc.InteractiveShellApp.exec_lines.append(\n    "try:\\n    %load_ext ip_object_browser\\nexcept ImportError: pass"\n)\nEOF\n```\n\n## Implementation\nBased on the [urwid](https://github.com/urwid/urwid) library,\nadapted from the [treesample example](https://github.com/urwid/urwid/blob/master/examples/treesample.py).\n\n## TODO\n- [ ] textual search functionality\n- [ ] status line with current path in object\n- [ ] path-based navigation\n- [ ] output current path on exit\n',
    'author': 'Roee Nizan',
    'author_email': 'roeen30@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roee30/ip_object_browser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
