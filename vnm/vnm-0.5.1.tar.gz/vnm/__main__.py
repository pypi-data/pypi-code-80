import argparse
import contextlib
import collections
import enum
import json
import logging
import os
import re
import shutil
import shlex
import string
import sys
import tempfile
import types
from pathlib import Path
from email.parser import BytesHeaderParser as EmailBytesHeaderParser
from email.message import EmailMessage
from typing import Tuple, List, Any, Dict
from ruamel.yaml import YAML

log = logging.getLogger(__name__)
if sys.version_info < (3, 6):
    print(f'CRITICAL: `{PROG}` MUST be run with Python 3.6 or higher. You are running v'+ ('.'.join(sys.version)))
    sys.exit(1)

from vnm.consts import PROG, NAME, VAR_PREFIX, DESC

import urllib.request
import urllib.parse
from typing import Optional, List
from subprocess import check_call, check_output, call, CalledProcessError, Popen, PIPE
from wheel.wheelfile import WheelFile

from vnm.repos import *
from vnm.constraint import Constraint
from vnm.package import Package
from vnm.state import ConfigState
from vnm.venv import activate, deactivate, setEnv, defined, unsetEnv

VENVDIR = os.path.abspath('.venv')
CORE_PACKAGES = ['pip', 'setuptools', 'wheel']

yaml = YAML(typ='rt')

def require_pipjson():
    if not os.path.isfile('pip.json') and not os.path.isfile('vnm.yml'):
        print('CRITICAL: I can\'t find pip.json nor vnm.yml!')
        sys.exit(1)

def require_venv():
    if 'VIRTUAL_ENV' not in os.environ:
        print(f'CRITICAL: This command must be run from a venv virtual environment. Did you run `{PROG} activate`? (VIRTUAL_ENV not set.)')
        sys.exit(1)

def getPython():
    pyexe = 'python.exe' if os.name == 'nt' else 'python'
    subdir = 'Scripts' if os.name == 'nt' else 'bin'
    return os.path.abspath(os.path.join(VENVDIR, subdir, pyexe))

def getPyPiVersionOf(packageid:str) -> str:
    xml = ''
    with urllib.request.urlopen(f'https://pypi.org/rss/project/{packageid}/releases.xml') as u:
        #<title>20.2b1</title>
        xml = u.read().decode('utf-8')
    #print(xml)
    m = re.search(r'<title>([0-9\.]+)</title>', xml)
    assert m is not None
    return m[1]

def update_package_manually(packageid, pkg: Optional[Package] = None, verbose: bool = False):
    if pkg is None:
        pkg = Package(packageid)
    if pkg.id == '':
        pkg.id = packageid
    cstr = pkg.constraintsToStr()
    if cstr == '':
        cstr = '(Newest)'
    print(f'Required {packageid} version: {cstr}')
    print(f'  Updating {packageid}...')
    #print(pkg.id, repr(pkg.serialize()))
    cmd = [getPython(), '-m', 'pip', 'install', '-U']+pkg.toPipArgs()
    if verbose: print('$', shlex.join(cmd))
    check_call(cmd)
    return pkg

def update_pip(pkg: Optional[Package] = None):
    if pkg is not None and len(pkg.constraints) > 0:
        update_package_manually('pip', pkg)
    else:
        upstream_version = getPyPiVersionOf('pip')
        o = check_output([getPython(), '-m', 'pip', '--version']).decode('utf-8')
        m = re.search(r'pip ([^ ]+) from (.*)', o)
        assert m is not None
        pip_version = m[1]
        print(f'Installed pip version: {pip_version}')
        print(f'Newest pip version: {upstream_version}')
        if upstream_version!=pip_version:
            print('  Updating pip...')
            check_call([getPython(), '-m', 'pip', 'install', '-U', 'pip'])

def check_core_pkgs(args: argparse.Namespace, cfg: ConfigState) -> None:
    print('Checking core packages...')
    update_pip(cfg.packages.get('pip'))
    for pkgid in CORE_PACKAGES:
        if pkgid == 'pip':
            continue
        update_package_manually(pkgid, cfg.packages.get(pkgid))

class EPipOperation(enum.IntEnum):
    INSTALL = enum.auto()
    REINSTALL = enum.auto()
    UPGRADE = enum.auto()

def install_venv(args: argparse.Namespace, cfg: ConfigState, operation=EPipOperation.INSTALL) -> List[Package]:
    pipargs = []
    verb = 'Installing'
    if operation == EPipOperation.REINSTALL:
        pipargs += ['-I']
        verb = 'Reinstalling'
    elif operation == EPipOperation.UPGRADE:
        pipargs += ['-U']
        verb = 'Upgrading'

    if len(cfg.packages) == 0 and len(cfg.dev_packages) == 0:
        return

    #check_core_pkgs(args, cfg)

    print('Writing temporary requirements file...')
    workdir = os.getcwd()
    tempfilename = ''
    all_packages: List[Package] = []
    try:
        if os.path.isfile('BROKEN-requirements.txt'):
            os.remove('BROKEN-requirements.txt')
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
            tempfilename = f.name
            packages = cfg.get_packages()
            for pkgid in CORE_PACKAGES:
                if pkgid in packages.keys():
                    packages[pkgid].priority = -1
            packages = packages.values()
            for pkg in sorted(packages, key=lambda p: (p.priority, p.id)):
                f.write(pkg.toRequirement()+'\n')
        print(f'{verb} packages from {tempfilename}...')
        check_call([getPython(), '-m', 'pip', 'install']+pipargs+['-r', tempfilename])
        '''
        with open(os.path.join(workdir, 'requirements.txt'), 'w') as f:
            for pid, pkg in cfg.packages.items():
                f.write(pkg.toRequirement()+'\n')
                all_packages += [pkg]
        with open(os.path.join(workdir, 'requirements-dev.txt'), 'w') as f:
            for pid, pkg in cfg.dev_packages.items():
                f.write(pkg.toRequirement()+'\n')
                all_packages += [pkg]
        '''
    except CalledProcessError as cpe:
        if os.path.isfile(tempfilename):
            shutil.copy(tempfilename, 'BROKEN-requirements.txt')
    finally:
        if os.path.isfile(tempfilename):
            os.remove(tempfilename)
    return all_packages

def update_requirements(cfg, args, all_packages):
    #print('update_requirements', cfg.generate_setup, cfg.generate_requirements)
    if cfg.generate_requirements or cfg.generate_setup:
        p = Popen([getPython(), '-m', 'pip', 'freeze'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        suffix = '-dev' if cfg.dev_mode else ''
        if p.returncode == 0:
            all_package_names = []
            pkgs = {}
            for pkg in cfg.get_all_packages().values():
                all_package_names += [pkg.id.lower()]
                pkgs[pkg.id.lower()] = pkg
            for line in stdout.splitlines():
                #print(line)
                #oline = line
                line = line.strip()
                p = Package(line.decode('utf-8'))
                pkg = None
                if p.id.lower() in CORE_PACKAGES:
                    continue
                if p.id.lower() in all_package_names:
                    pkg = pkgs[p.id.lower()]
                #else:
                #    f.write(f'#{p.toRequirement()}\n')
                if pkg is not None:
                    if len(pkg.constraints) == 0:
                        pkg.constraints = p.constraints
                    if isinstance(pkg.repo, GitRepo) and isinstance(p.repo, GitRepo) and pkg.repo.refid != p.repo.refid:
                        pkg.repo = p.repo
                #print(line, pkg.id if pkg is not None else None, json.dumps(pkg.serialize()) if pkg is not None else None)

            for pkgid in CORE_PACKAGES:
                p = Package(pkgid)

                c = Constraint()
                c.setEquality('==')
                c.setVersion(get_local_pkg_version(p.id))
                #print(f'Adding constraint {c.toRequirement()} to package {p.id}')
                p.constraints += [c]

                pkg = None
                if pkgid in all_package_names:
                    pkg = pkgs[p.id]

                if pkg is not None:
                    if len(pkg.constraints) == 0:
                        pkg.constraints = p.constraints
                    if isinstance(pkg.repo, GitRepo) and isinstance(p.repo, GitRepo) and pkg.repo.refid != p.repo.refid:
                        pkg.repo = p.repo

            all_release_pkgs = [k.lower() for k in cfg.packages.keys()]
            all_pkgs = all_release_pkgs+[k.lower() for k in cfg.dev_packages.keys()]

            if cfg.generate_setup:
                print('Writing setup.cfg')
                cfg.update_setup(args, all_release_pkgs, all_pkgs, pkgs)

            if cfg.generate_requirements:
                print('Writing requirements')
                fdev = contextlib.nullcontext()
                if cfg.dev_mode:
                    fdev = open(f'requirements-dev.new.txt' if args.dry_run else f'requirements-dev.txt', 'w')
                with open(f'requirements.new.txt' if args.dry_run else f'requirements.txt', 'w') as frel:
                    with fdev:
                        frel.write(f'# Generated by vnm\n')
                        if cfg.dev_mode:
                            fdev.write(f'# Generated by vnm\n')
                        for pkg in sorted(pkgs.values(), key=lambda p: p.priority):
                            if pkg.id.lower() in all_release_pkgs:
                                #frel.write(f'#{pkg.priority}\n')
                                frel.write(f'{pkg.toRequirement()}\n')
                            if cfg.dev_mode and pkg.id.lower() in all_pkgs:
                                fdev.write(f'{pkg.toRequirement()}\n')


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    argp = argparse.ArgumentParser(prog=PROG, description=DESC)
    argp.add_argument('--dry-run', action='store_true', default=False, help='Don\'t actually do anything.')
    subp = argp.add_subparsers()

    p_upgrade = subp.add_parser('upgrade', aliases=['u'], help='Upgrade all packages defined in vnm.yml to their latest available versions.')
    p_upgrade.set_defaults(cmd=_cmd_upgrade)

    p_upgrade_config = subp.add_parser('upgrade-config', help='Upgrade from pip.json to vnm.yml.')
    p_upgrade_config.set_defaults(cmd=_cmd_upgrade_config)

    p_import_setup = subp.add_parser('import-setup', help='Import setup.cfg')
    p_import_setup.add_argument('filename', default='setup.cfg', nargs='?', help="Alternate name for the .cfg file.")
    p_import_setup.set_defaults(cmd=_cmd_import_setup)

    p_install = subp.add_parser('install', aliases=['i'], help='Install all packages defined in vnm.yml')
    p_install.add_argument('--dev', '-d', action='store_true', default=False, help='Install in development mode. (Adds dev-packages.)')
    p_install.set_defaults(cmd=_cmd_install)

    p_init = subp.add_parser('init', help='Set up an initial .venv and vnm.yml.')
    p_init.add_argument('--clobber', action='store_true', default=False, help="Forcefully reinstall .venv and vnm.yml.")
    p_init.add_argument('--git', action='store_true', default=False, help="Setup git and add necessary excludes and ignores.")
    p_init.add_argument('--lfs', action='store_true', default=False, help="Setup git lfs, as well.")
    p_init.set_defaults(cmd=_cmd_init)

    p_add = subp.add_parser('add', help='Add a dependency to vnm.yml')
    p_add.add_argument('package', nargs='+', help="A package name or pip URI.")
    p_add.add_argument('--dev', '-d', action='store_true', default=False, help='All packages provided are development packages.')
    p_add.add_argument('--editable', '-e', nargs='+', type=str, help="A package name or pip URI (installed with -e).")
    p_add.add_argument('--force-reinstall', action='store_true', default=False, help="Forcefully reinstall all packages.")
    p_add.set_defaults(cmd=_cmd_add)

    p_remove = subp.add_parser('remove', aliases=['rm'], help='Remove package(s)')
    p_remove.add_argument('package', nargs='+', help="Package names.")
    p_remove.add_argument('--dev', '-d', action='store_true', default=False, help='All packages provided are development packages.')
    p_remove.set_defaults(cmd=_cmd_remove)

    p_activate = subp.add_parser('activate', aliases=['a'], help='Activate virtual environment.')
    p_activate.set_defaults(cmd=_cmd_activate)

    p_freeze = subp.add_parser('freeze', aliases=['f'], help='Freeze package version.')
    p_freeze.add_argument('packages', nargs='*', help="Package names.")
    p_freeze.set_defaults(cmd=_cmd_freeze)

    p_thaw = subp.add_parser('thaw', aliases=['t'], help='Thaw package version.')
    p_thaw.add_argument('packages', nargs='*', help="Package names.")
    p_thaw.add_argument('--constraints', action='store_true', default=False, help="Also wipe all version constraints.")
    p_thaw.set_defaults(cmd=_cmd_thaw)

    p_run = subp.add_parser('run', aliases=['r'], help='Run a python script in the virtual environment.')
    p_run.add_argument('filename', help='The python script or command to run')
    p_run.add_argument('args', nargs=argparse.REMAINDER, help='The python script to run')

    p_dumpenv = subp.add_parser('dump-env', help='Dump current environment variables.')
    p_dumpenv.add_argument('--format', choices=['text', 'json'], default='text', help='Format to output in')
    p_dumpenv.set_defaults(cmd=_cmd_dump_env)

    args = argp.parse_args()

    if getattr(args, 'cmd', None) is None:
        argp.print_usage()
    else:
        args.cmd(args)

def _sort_dict(d: dict) -> dict:
    nd = collections.OrderedDict()
    for k in sorted(d.keys()):
        nd[k]=d[k]
    return dict(nd)

def _cmd_add(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    newpkgs = []
    all_packages = []
    for packagedef in args.package:
        pkg = Package(packagedef)
        print(f'Adding {pkg}...')
        if pkg.id not in (None, '') and pkg.id in cfg.packages:
            print(f'WARNING: Package {pkg.id!r} exists in {cfg.get_filename()}.')
        if args.dev:
            cfg.dev_packages[pkg.id] = pkg
        else:
            cfg.packages[pkg.id] = pkg
        if (cfg.dev_mode and args.dev) or (not cfg.dev_mode and not args.dev):
            newpkgs += pkg.toPipArgs()

    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

    # Same as _cmd_install().
    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def get_local_pkg_version(pkgid: str) -> str:
    # I don't know why they did this.
    o: bytes = check_output([getPython(), '-m', 'pip', 'show', pkgid])
    headers: EmailMessage = EmailBytesHeaderParser().parsebytes(o)
    #print(repr(dict(headers)))
    return headers.get('Version')

def _cmd_freeze(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    pkgs_to_freeze = []
    for packagedef in args.packages:
        pkg = Package(packagedef)
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'WARNING: Package {pkg.id!r} not specified in vnm.yml/pip.json.')
        pkgs_to_freeze += [pkg.id]

    p = Popen([getPython(), '-m', 'pip', 'freeze', '--all'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    suffix = '-dev' if cfg.dev_mode else ''
    if p.returncode == 0:
        all_package_names = []
        pkgs = {}
        for pkg in cfg.get_all_packages().values():
            all_package_names += [pkg.id.lower()]
            pkgs[pkg.id.lower()] = pkg
        for line in stdout.splitlines():
            #print(line)
            #oline = line
            line = line.strip()
            p = Package(line.decode('utf-8'))
            pkg = None
            if p.id.lower() in all_package_names:
                pkg = pkgs[p.id.lower()]

            if pkg is None:
                print(f'{p.id} not in package list.')
                continue

            if len(pkgs_to_freeze) == 0 or pkg.id in pkgs_to_freeze:
                if len(p.constraints) == 0:
                    if p.repo and hasattr(p.repo, 'refid') and p.repo.reftype == EGitRefType.COMMIT:
                        c = Constraint()
                        c.setEquality('==')
                        c.setVersion(p.repo.refid)
                        print(f'Adding constraint {c.toRequirement()}')
                        p.constraints += [c]
                        print(f'Removing refid {p.repo.refid}')
                        p.repo.refid = None
                        p.repo.reftype = None
                    else:
                        print(f'WARNING: Package {p.id} has no version info. Grabbing from pip show instead.')
                        c = Constraint()
                        c.setEquality('==')
                        c.setVersion(get_local_pkg_version(p.id))
                        print(f'Adding constraint {c.toRequirement()}')
                        p.constraints += [c]
                        #continue
                if len(p.constraints) > 1:
                    pc = ', '.join([x.toRequirement() for x in p.constraints])
                    print(f'WARNING: Package {p.id} has a bunch of constraints. ({pc}) Grabbing from pip show instead.')
                    c = Constraint()
                    c.setEquality('==')
                    c.setVersion(get_local_pkg_version(p.id))
                    print(f'Settng constraints to {c.toRequirement()}')
                    p.constraints = [c]
                    #continue
                pkg.freezeAt(p.constraints[0])
                if isinstance(pkg.repo, GitRepo) and isinstance(p.repo, GitRepo):
                    pkg.repo.uri = p.repo.uri

                if pkg.id in cfg.dev_packages.keys():
                    print(f'Freezing dev package {pkg.id!r}')
                    cfg.dev_packages[pkg.id].freezeAt(p.constraints[0])
                if pkg.id in cfg.packages.keys():
                    print(f'Freezing package {pkg.id!r}')
                    cfg.packages[pkg.id].freezeAt(p.constraints[0])


    cfg.saveState()
    cfg.saveVNM()

    # Same as _cmd_install().
    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_thaw(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    pkgs_to_thaw = []
    for packagedef in args.packages:
        pkg = Package(packagedef)
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'WARNING: Package {pkg.id!r} not specified in vnm.yml/pip.json.')
        pkgs_to_thaw += [pkg.id.lower()]

    for pkg in cfg.dev_packages.values():
        if len(args.packages) == 0 or pkg.id.lower() in pkgs_to_thaw:
            print(f'Thawing dev package {pkg.id!r}')
            pkg.thaw()
            if args.constraints:
                pkg.constraints = []
    for pkg in cfg.packages.values():
        if len(args.packages) == 0 or pkg.id.lower() in pkgs_to_thaw:
            print(f'Thawing package {pkg.id!r}')
            pkg.thaw()
            if args.constraints:
                pkg.constraints = []

    cfg.saveState()
    cfg.saveVNM()

    # Same as _cmd_install().
    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_import_setup(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    path = Path(args.filename)
    print('Importing {path}...')
    cfg.import_setup(path)

    cfg.saveState()
    cfg.saveVNM()

    # Same as _cmd_install().
    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_remove(args) -> None:
    require_venv()

    cfg = ConfigState()
    cfg.load()

    rmpkgs = []
    all_packages = []
    for packagedef in args.package:
        pkg = Package(packagedef)
        print(f'Removing {pkg}...')
        if pkg.id not in (None, '') and pkg.id not in cfg.get_all_packages():
            print(f'  WARNING: Package {pkg.id} not specified in vnm.yml/pip.json.')
        if pkg.id in cfg.packages:
            del cfg.packages[pkg.id]
        if pkg.id in cfg.dev_packages:
            del cfg.dev_packages[pkg.id]
        rmpkgs += [pkg.id]

    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

    # Same as _cmd_install().
    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    call([getPython(), '-m', 'pip', 'uninstall', '-y']+rmpkgs)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_upgrade(args):
    require_venv()
    require_pipjson()

    cfg = ConfigState()
    cfg.load()

    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg, operation=EPipOperation.UPGRADE)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_upgrade_config(args):
    require_pipjson()

    cfg = ConfigState()

    if os.path.isfile('pip.json'):
        print('WARNING: Upgrading pip.json to vnm.yml...')
        if not os.path.isfile('pip.json.bak'):
            print('Backing up pip.json to pip.json.bak...')
            shutil.copy('pip.json', 'pip.json.bak')
        else:
            print("pip.json.bak exists, skipping backup.")
        print('Reading...')
        cfg.load()
        if not args.dry_run:
            print('Removing pip.json...')
            os.remove('pip.json')
    elif os.path.isfile('vnm.yml'):
        print('WARNING: Upgrading vnm.yml...')
        if not os.path.isfile('vnm.yml.bak'):
            print('Backing up vnm.yml to vnm.yml.bak...')
            shutil.copy('vnm.yml', 'vnm.yml.bak')
        else:
            print("vnm.yml.bak exists, skipping backup.")
        print('Reading...')
        cfg.load()
    else:
        print('CRITICAL: Neither vnm.yml nor pip.json are present.  Exiting.')
        sys.exit(1)
    print('Writing vnm.yml...')
    cfg.as_json = False
    cfg.saveState(args.dry_run)
    cfg.saveVNM(args.dry_run)

def _cmd_install(args):
    if not os.path.isfile('vnm.yml'):
        if not os.path.isfile('pip.json'):
            print(f'CRITICAL: vnm.yml is missing.  This project is not set up for {NAME}.')
            return
        print('WARNING: pip.json is deprecated.')
    if not os.path.isfile(getPython()):
        print('WARNING: Virtual environment not installed. Initializing...')
        clear_cmd = [sys.executable, '-m', 'venv']
        if os.path.isdir('.venv'):
            clear_cmd += ['--clear']
        clear_cmd += ['.venv']
        clear_cmd_str = ' '.join(clear_cmd)
        print(f'Running {clear_cmd_str}...')
        check_call(clear_cmd, shell=False)
    #require_venv()
    require_pipjson()

    cfg = ConfigState()
    cfg.load()
    cfg.dev_mode = args.dev
    cfg.saveState()

    activate(VENVDIR)
    check_core_pkgs(args, cfg)
    all_packages = install_venv(args, cfg)
    deactivate(VENVDIR)

    update_requirements(cfg, args, all_packages)

def _cmd_init(args):
    if (os.path.isfile('pip.json') or os.path.isfile('vnm.yml')) and not args.clobber:
        print('CRITICAL: pip.json or vnm.yml exists, aborting.  If you REALLY want to re-init the project, please set --clobber.')
        return

    print('Cleaning up prior install...')
    if os.path.isfile('pip.json'):
        print('rm pip.json')
        os.remove('pip.json')
    if os.path.isfile('vnm.yml'):
        print('rm vnm.yml')
        os.remove('vnm.yml')
    clear_cmd = [sys.executable, '-m', 'venv', '--clear', '.venv']
    clear_cmd_str = ' '.join(clear_cmd)
    print(f'Running {clear_cmd_str}...')
    check_call(clear_cmd)

    print('Writing vnm.yml...')
    cfg = ConfigState()
    cfg.saveVNM()
    cfg.saveState()

    if args.git:
        if not os.path.isdir('.git'):
            print('Running git init...')
            check_call(['git', 'init'])
            if args.lfs:
                print('Running git lfs install...')
                check_call(['git', 'lfs', 'install'])
        if not os.path.isfile('.gitignore'):
            print('Writing .gitignore...')
            with open('.gitignore', 'w') as f:
                f.write('# vnm files\n/vnm.state\n/.venv/\n\n# general python stuff\n*.py[ioc]\n/*.egg-info/\n')

    #check_core_pkgs(args, cfg)
    print( '********************************************************************')
    print(f'.venv for {NAME} installed!')
    print( 'Next steps:')
    print(f'  1. Run `{PROG} activate` to activate the virtual environment.')
    print(f'  2. Add packages with `{PROG} add <package>` OR edit .')
    print( '  3. Add vnm.yml and requirements.txt to your VCS (if applicable).')
    print( '********************************************************************')

def _cmd_dump_env(args):
    data = {
        'os.environ':os.environ,
        'sys.path':sys.path,
    }
    if args.format == 'json':
        print(json.dumps(data))
    else:
        print('os.environ:')
        for key, value in os.environ.items():
            print(f'  {key}: {value!r}')
        print('sys.path:')
        for value in sys.path:
            print(f'  - {value}')

def _cmd_activate(args):
    if not os.path.isfile(getPython()):
        print(f'CRITICAL: Virtual environment not installed. Did you run `{PROG} init`?', PROG)
        return
    if f'_{VAR_PREFIX}_ACTIVE' in os.environ:
        log.critical(f'You are already in a {NAME} virtual environment, you doofus.')
        sys.exit(1)
        return

    if os.name == 'nt':
        _cmd_activate_nt(args)
    else:
        _cmd_activate_bash(args)

def _cmd_activate_nt(args):
    activate(VENVDIR)
    oldprompt = os.environ['PROMPT']
    os.environ['PROMPT'] = f'[{NAME}] {oldprompt}'
    print('='*60)
    print('Great, all done.')
    print('You are now in a child cmd.exe shell with the virtual environment set up for you.')
    print('You can deactivate the environment at any time by using the `exit` command.')
    print('='*60)
    def hide_script(a):
        if os.path.isfile(a):
            if os.path.isfile(a+'bak'):
                os.remove(a+'.bak')
            shutil.move(a, a+'.bak')
    def unhide_script(a):
        if os.path.isfile(a):
            os.remove(a)
        shutil.move(a+'.bak', a)
    hide_script(os.path.join(VENVDIR, 'Scripts', 'deactivate.bat'))
    code = -1
    try:
        #code = call(['cmd.exe', '/k', os.path.join(VENVDIR, 'Scripts', 'deactivate.bat')], shell=True)
        code = call(['cmd.exe'], shell=True)
    finally:
        print(f'{PROG}: cmd.exe exited with code {code}')
        unhide_script(os.path.join(VENVDIR, 'Scripts', 'deactivate.bat'))
        deactivate(VENVDIR)
        os.environ['PROMPT'] = oldprompt

def _cmd_activate_bash(args):
    filename = ''
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        filename = f.name

        def writeNDebug(line):
            log.debug('Writing %r...', line)
            f.write(line)

        writeNDebug('echo "Activating..."\n')

        writeNDebug(f'. ~/.bashrc\n')
        writeNDebug(f'. {VENVDIR}/bin/activate\n')

        # Don't want users escaping by the normal means
        writeNDebug(f'unset -f deactivate\n')
        writeNDebug('alias deactivate=exit\n')
        writeNDebug(f'export _{VAR_PREFIX}_ACTIVE=1\n')
        writeNDebug(f'export _{VAR_PREFIX}_PROCESS={os.getpid()}\n')
        writeNDebug(f'PS1="[{NAME}] ${{PS1}}"\n')

        bar = '='*60
        writeNDebug(f'echo "{bar}"\n')
        writeNDebug('echo "Great, all done."\n')
        writeNDebug('echo "You are now in a child bash shell with the virtual environment set up for you."\n')
        writeNDebug('echo "You can deactivate the environment at any time by using the \\`exit\\` command."\n')
        writeNDebug(f'echo "{bar}"\n')
    code = call(['/bin/bash', '--init-file', filename])
    print(f'{PROG}: bash exited with code {code}')
    os.remove(filename)


#def _cmd_deactivate(args):
#    from vnm.venv import deactivate
#    deactivate('.venv')

def _cmd_run(args):
    from vnm.venv import runFrom
    runFrom('.venv', args.filename, args.args)

if __name__ == '__main__':
    main()
