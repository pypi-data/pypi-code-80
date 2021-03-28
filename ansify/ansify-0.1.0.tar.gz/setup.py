# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ansify']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'numpy>=1.19.5,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.0.0,<11.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'urwid>=2.1.2,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['ansify = ansify.__main__:app']}

setup_kwargs = {
    'name': 'ansify',
    'version': '0.1.0',
    'description': 'Awesome `ansify` is a Python CLI to create ANSI/ASCII art from images.',
    'long_description': '# ansify\n\n<div align="center">\n\n[![Build status](https://github.com/lonsty/ansify/workflows/build/badge.svg?branch=master&event=push)](https://github.com/lonsty/ansify/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/ansify.svg)](https://pypi.org/project/ansify/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/lonsty/ansify/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/lonsty/ansify/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/lonsty/ansify/releases)\n[![License](https://img.shields.io/github/license/lonsty/ansify)](https://github.com/lonsty/ansify/blob/master/LICENSE)\n\nAwesome `ansify` is a Python CLI to create ANSI/ASCII art from images.\n\n好玩的终端图片艺术工具\n\n</div>\n\n## 工具特点\n\n- [X] 任意图片转成任意字符\n- [X] 支持彩色输出\n\n## 使用说明\n\n### 安装工具 ansify\n\n```bash\npip install -U ansify\n```\n\n### Let\'s go\n\n原图\n\n![](examples/ycy.jpg)\n\n- 黑白\n\n```bash\nansify --columns 120 --no-color examples/ycy.jpg\n```\n\n![](examples/demo_ycy_1.png)\n\n- 彩色\n\n```bash\nansify --columns 120 examples/ycy.jpg\n```\n\n![](examples/demo_ycy_2.png)\n\n- 像素\n\n```bash\nansify --columns 120 --grayscale pixel examples/ycy.jpg\n```\n\n![](examples/demo_ycy_3.png)\n\n- 自定义字符\n\n```bash\nansify --columns 120 --diy-grayscale "你我爱超越" examples/ycy.jpg\n```\n\n![](examples/demo_ycy_4.png)\n\n- 其他示例\n\n\n```bash\nansify --columns 80 --diy-grayscale " 谁咬我苹果" examples/apple.png\n```\n\n![](examples/demo_apple_1.png)\n\n\n```bash\nansify --columns 80 --grayscale emoji examples/apple.png\n```\n\n![](examples/demo_apple_2.png)\n\n```bash\nansify https://b-ssl.duitang.com/uploads/item/201712/06/20171206200408_txunr.thumb.700_0.jpeg\n```\n\n![](examples/demo_bilibili_1.png)\n\n### 参数说明\n\n```bash\n$ ansify --help\nUsage: ansify [OPTIONS] IMAGE\n\n  CLI to create ANSI/ASCII art from images.\n\nArguments:\n  IMAGE  Image file PATH or URL.  [required]\n\nOptions:\n  -c, --columns INTEGER           Output columns, number of characters per\n                                  line.  [default: 252]\n\n  -o, --output PATH               Save ANSI/ASCII art to the OUTPUT file.\n  -s, --scale FLOAT               The larger the scale, the thinner the art.\n                                  [default: 0.43]\n\n  -g, --grayscale [simple|morelevels|pixel|dragon|emoji]\n                                  Choose a built-in gray scale.  [default:\n                                  simple]\n\n  -d, --diy-grayscale TEXT        Customize your gray scale.\n  -n, --no-color                  Output a ANSI/ASCII art without color.\n                                  [default: False]\n\n  -r, --reverse-grayscale         Reverse the grayscale.  [default: False]\n  -R, --reverse-color             Reverse the color.  [default: False]\n  -q, --quite                     Hide output information.  [default: False]\n  -v, --version                   Prints the version of the ansify package.\n  --help                          Show this message and exit.\n```\n必要参数：\n\n- `IMAGE`: 本地图片文件路径，或者网络图片 URL\n\n可选参数：\n\n- `-c, --columns`：转化后图片的列数（汉字占两个字符，列数会减半），默认为终端的宽度\n- `-o, --output`：指定文件名如 `output.txt` 后，将输出字符保存到文件\n- `-s, --scale`：受终端配置（字间距、行高）与字符长宽比的影响，输出图像的长宽比与原图有差别。必要时使用此参数调整长宽比，该值越大，图片越高瘦\n- `-g, --grayscale`：预设的几种灰阶递增（字符越来越密集）字符，`[simple|morelevels|pixel|dragon|emoji]`\n- `-d, --diy-grayscale`：自定义灰阶字符，可以是单字符，多字符最好灰阶递增或递减\n- `-n, --no-color`：禁用彩色\n- `-r, --reverse-grayscale`：灰阶字符反转，终端背景为亮色时可以试试看\n- `-R, --reverse-color`：颜色反转\n- `-q, --quite`：输出结果中，屏蔽除字符图的其他信息\n\n其他：\n\n- `-v, --version`：打印工具版本信息\n- `--help`：打印工具使用说明\n\n## Release History\n\n### 1.0.0\n\nInitial release on PyPI.\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/lonsty/ansify)](https://github.com/lonsty/ansify/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/lonsty/ansify/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{ansify,\n  author = {lonsty},\n  title = {Awesome `ansify` is a Python CLI to create ANSI/ASCII art from images.},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/lonsty/ansify}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'lonsty',
    'author_email': 'lonsty@sina.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lonsty/ansify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
