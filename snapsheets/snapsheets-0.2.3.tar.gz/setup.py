# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snapsheets']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.12,<2.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'icecream>=2.1.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'snapsheets',
    'version': '0.2.3',
    'description': 'Wget snapshots of google sheets',
    'long_description': '![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n\n# Snapsheets\n\nWget snapshots of Google Spreadsheets\n\nThis package enables to wget Google Spreadsheets without login.\n(Spreadsheets should be shared with public link)\n\n\n---\n\n# Usage\n\n```python\n>>> import snapsheets as ss\n>>> ss.add_config(\'test_config.yml\')\n>>> ss.get(\'test1\', by=\'wget\')\n```\n\n---\n\n## Config\n\n- Write config file in ``YAML`` format\n\n```yaml\nvolumes:\n  snapd: \'data/\'\n\noptions:\n  wget:\n    \'--quiet\'\n\nsheets:\n  test1:\n    key: \'1NbSH0rSCLkElG4UcNVuIhmg5EfjAk3t8TxiBERf6kBM\'\n    gid: \'None\'\n    format: \'xlsx\'\n    sheet_name:\n      - \'シート1\'\n      - \'シート2\'\n    stem: \'test_sheet\'\n    datefmt: \'%Y\'\n```\n\n---\n\n# Documents\n\n- https://shotakaha.gitlab.io/snapsheets/\n\n---\n\n# Snapsheets\n\nWget snapshots of Google spreadsheet\n\n---\n\n![GitLab pipeline](https://img.shields.io/gitlab/pipeline/shotakaha/snapsheets?style=for-the-badge)\n![PyPI - Licence](https://img.shields.io/pypi/l/snapsheets?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/snapsheets?style=for-the-badge)\n![PyPI - Status](https://img.shields.io/pypi/status/snapsheets?style=for-the-badge)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/snapsheets?style=for-the-badge)\n\n---\n\n![PyPI - Downloads](https://img.shields.io/pypi/dd/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dw/snapsheets?style=for-the-badge)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/snapsheets?style=for-the-badge)\n\n---\n\n# Usage\n\n```python\n>>> import snapsheets as ss\n>>> ss.add_config(\'config.yml\')\n>>> ss.get(\'test1\', by=\'wget\')\n```\n\n# Install\n\n```bash\n$ pip3 install snapsheets\n```\n\n# Documents\n\n- https://shotakaha.gitlab.io/snapsheets/\n\n---\n\n# 設定ファイルの項目\n\n- ``volumes`` : 保存先\n- ``options`` : ダウンロード時のオプション\n- ``sheets`` : スプレッドシートの情報\n\n## ``volumes`` : 保存先\n\n- ダウンロードしたスプレッドシートを保存する場所を設定する項目\n- いまは ``snapd`` だけ必要\n- デフォルトはカレントディレクトリ\n\n```yaml\nvolumes:\n  snapd: "."\n```\n\n## ``options`` : ダウンロード時のオプション\n\n- ダウンロード時のオプションを設定する項目\n- いまは ``wget`` だけ必要\n\n```yaml\noptions:\n  wget:\n    \'--quiet\'\n```\n\n## ``sheets`` : スプレッドシートの情報\n\n- スプレッドシートの情報を設定する項目\n- 複数のスプレッドシートを設定できる\n\n```yaml\nsheets:\n  シートの名前:\n    key: スプレッドシート全体のID\n    gid: ダウンロードするシートのID\n    format: ダウンロード形式\n    sheet_name:\n      - \'シートの名前\'\n    stem: \'バックアップ時につけるファイル名\'\n    datefmt: \'バックアップ時に使う日付フォーマット\'\n```\n\n### ``datefmt`` : 日付フォーマット\n\n- バックアップする際のファイル名につける日付プリフィックス\n- デフォルトは ``%Y%m%dT%H%M%S``\n\n\n---\n\n\n# 開発用メモ\n\n## ローカルでテストする場合\n\n```bash\n$ git clone https://gitlab.com/shotakaha/snapsheets.git\n$ cd snapsheets/python/\n$ pip3 install .\n$ pip3 show snapsheets\n```\n\n## Test PyPI のテストをする場合\n\n```bash\n$ pip3 install -i https://test.pypi.org/simple/\n$ pip3 show snapsheets\n```\n\n\n---\n\n# Test PyPI への登録\n\n- https://test.pypi.org/project/snapsheets/\n- API Token を発行する\n  - ``API Token``は一度しか発行できない（忘れてしまったら再発行するしかない？）\n  - ``$HOME/.pypirc``に設定を保存しておく\n\n## アップロード\n\n```bash\n$ cd python/\n$ rm -r dist/\n$ python3 setup.py sdist bdist_wheel\n$ twine upload --repository testpypi dist/*\nUploading distributions to https://test.pypi.org/legacy/\nEnter your username: __token__\nEnter your password: ## APIトークンをコピペ\n```\n\n---\n\n# PyPI への登録\n\n- https://pypi.org/project/snapsheets/\n- API Token を発行する\n  - ``API Token``は一度しか発行できない（忘れてしまったら再発行するしかない？）\n  - ``$HOME/.pypirc``に設定を保存しておく\n\n## アップロード\n\n```bash\n$ cd python/\n$ rm -r dist/\n$ python3 setup.py sdist bdist_wheel\n$ twine upload dist/*\nUploading distributions to https://pypi.org/legacy/\n```\n\n---\n\n# ``$HOME/.pypirc`` の設定\n\n- 以下の記事を参照\n- https://truveris.github.io/articles/configuring-pypirc/\n\n```conf\n[distutils]\n  index-servers=\n      pypi\n      testpypi\n\n[testpypi]\n  repository: https://test.pypi.org/legacy/\n  username = __token__\n  password = pypi-****\n\n[pypi]\n  username = __token__\n  password = pypi-****\n```\n\n---\n\n## ``TestPyPI``にアップロードしたときに分かったこと／気をつける点\n\n- メールアドレス（``setup.py``に書く``author_email``）は、``TestPyPI``に登録したメールアドレスでなくてもOKだった\n  - ``valid``な文字列であればなんでもよいみたい\n  - ``invalid``なアドレスは``twine``でエラーがでる（``xxxxxx``にしてたら怒られた）\n- 同じ名前のファイルは登録することができない\n  - https://test.pypi.org/help/#file-name-reuse を参照\n  - ``twine upload``する前に ``dist/*`` を空っぽにしたほうがよい\n  - リビジョン番号は、当面``Test PyPi``の表示確認ように使うことにする\n',
    'author': 'shotakaha',
    'author_email': 'shotakaha+py@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://shotakaha.gitlab.io/snapsheets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
