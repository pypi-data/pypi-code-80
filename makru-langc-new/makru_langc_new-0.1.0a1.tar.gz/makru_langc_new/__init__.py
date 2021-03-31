# Copyright (C) 2021 Jin Wa, and the project contributors
# 
# This file is part of makru_langc_new.
# 
# makru_langc_new is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#  any later version.
# 
# makru_langc_new is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with makru_langc_new.  If not, see <http://www.gnu.org/licenses/>.
from clint import Args
from clint.textui import prompt, puts_err, puts
from typing import Dict, Any, TypeVar
from pathlib import Path
from makru.helpers import shell
from makru.yamlh import dump
from makru.nethelpers import download

T = TypeVar('T')

GIT_IGNORES_URL = "https://github.com/github/gitignore/blob/master/C.gitignore?raw=true"

def get_makru_config_content(name: str, version: str, type: str) -> Dict[str, Any]:
    BASE_MAKRU_CONFIG = {
        'name': None,
        'use': 'makru_langc',
        'version': None,
        'type': None,
        'language_c': {
            'std': 'c11',
            'sources': [
                'src/**'
            ],
            'resolvers': [
                'pkgconf',
                'system',
            ]
        },
        'actions': {
            'resolve_dependencies': 'makru_langc:resolve_dependencies',
            'run': 'makru_langc:run',
            'envinfo': 'makru_langc:envinfo',
        }
    }
    BASE_MAKRU_CONFIG['name'] = name
    BASE_MAKRU_CONFIG['version'] = version
    BASE_MAKRU_CONFIG['type'] = type
    return BASE_MAKRU_CONFIG

def install_makru_langc_git_module(target: Path):
    if not (target / '.git').exists():
        shell(('git', 'init'), cwd=str(target))
    shell(('git', 'submodule', 'add', 'https://gitlab.com/jinwa/makru_langc.git', 'makru/plugins/makru_langc'), cwd=str(target), non_zero_to_fail=True)

def write_makru_config(target: Path, **kwargs):
    content = get_makru_config_content(**kwargs)
    path = (target / 'makru.yaml')
    with path.open('w+') as f:
        dump(content, f)

def create_directory_layout(target: Path):
    (target / 'src').mkdir(parents=True, exist_ok=True)
    (target / 'makru' / 'plugins').mkdir(parents=True, exist_ok=True)
    (target / 'include').mkdir(parents=True, exist_ok=True)

def setup_gitignore(target: Path):
    puts('Downloading .gitignore from "{}"...'.format(GIT_IGNORES_URL))
    path = target / '.gitignore'
    download(GIT_IGNORES_URL, str(path), show_progress=True)

def _main():
    args = Args()
    if args.all_with('-h') or args.all_with('--help'):
        puts("makru_langc_new TARGET [-Nname] [-Vversion] [-Ttype] [-h/--help]")
        return
    if not args.not_flags:
        puts("a target directory is required")
        raise RuntimeError("no target")
    target = args.not_flags.all[0]
    target_path = Path(target)
    name = args.all_with("-N")[-1]
    name = name[2:] if name else None
    version = args.all_with('-V')[-1]
    version = version[2:] if version else None
    p_type = args.all_with('-T')[-1]
    p_type = p_type[2:] if p_type else None
    if not name:
        name = prompt.query("Project name:", default=target)
    if not version:
        version = prompt.query("Project version:", default='0.1.0')
    if not p_type:
        p_type = prompt.query("Project type (executable or library for common workflow):", default='library')
    create_directory_layout(target_path)
    install_makru_langc_git_module(target_path)
    write_makru_config(target_path, name=name, version=version, type=p_type)
    setup_gitignore(target_path)

def main():
    import sys
    try:
        _main()
    except Exception as e:
        puts_err(str(e))
        sys.exit(127)
