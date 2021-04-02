import os
import types
import json
import logging
import collections
import argparse
import configparser
from typing import Tuple, List, Any, Dict, Optional, Callable
from ruamel.yaml import YAML

from setuptools.config import read_configuration

from vnm.consts import PROG, NAME, VAR_PREFIX, DESC

log = logging.getLogger(__name__)

yaml = YAML(typ='rt')

from vnm.constraint import Constraint
from vnm.package import Package

class ConfigState(object):
    PIPJSON_VERSION = 1
    VNMYML_VERSION = 4
    STATE_FILENAME = 'vnm.state'
    STATE_VERSION = '202103291800'

    def __init__(self, args: Optional[argparse.Namespace] = None) -> None:
        self.as_json: bool = False
        self.dev_mode: bool = False
        self.generate_requirements: bool = False
        self.generate_setup: bool = False

        self.egginfo: dict = {}

        self.packages: Dict[str, Package] = {}
        self.dev_packages: Dict[str, Package] = {}

        self.yaml_upgrades: Dict[int, Callable] = {}
        self.state_upgrades: Dict[Any, Callable] = {}

        def addVnmYamlUpgrade(forVersion: int):
            def _wrap(process: callable) -> callable:
                self.yaml_upgrades[forVersion] = process
                return process
            return _wrap

        @addVnmYamlUpgrade(1)
        def vnmYmlv2(docs):
            docs[0]={'VERSION': 2}
            return docs

        @addVnmYamlUpgrade(2)
        def vnmYmlv3(docs):
            newdoc = {
                'version': 3,
                'packages': docs[1]['packages']
            }
            if 'dev-packages' in docs[1]:
                newdoc['dev-packages'] = docs[1]['dev-packages']
            return [newdoc]

        @addVnmYamlUpgrade(3)
        def vnmYmlv4(docs):
            newdoc = {
                'version': 4,
                'package-info': {},
                'options': {
                    'generate_setup': False,
                    'generate_requirements': True,
                }
            }
            if 'packages' in docs[0]:
                newdoc['packages'] = docs[0]['packages']
            if 'dev-packages' in docs[0]:
                newdoc['dev-packages'] = docs[0]['dev-packages']
            return [newdoc]

        def addVnmStateUpgrade(forVersion: Any):
            def _wrap(process: callable) -> callable:
                self.state_upgrades[forVersion] = process
                return callable
            return _wrap

        @addVnmStateUpgrade('202006122014')
        def vnmState_2020_07_13_1859(docs):
            return ['202007131859', docs[2]]

    def get_filename(self) -> str:
        if self.as_json:
            return 'vnm.json'
        else:
            return 'vnm.yml'

    def getYamlVersion(self, docs) -> int:
        # 202006122014
        #if isinstance(docs, )
        if isinstance(docs, list):
            if isinstance(docs[0], int):
                return docs[0]
            elif isinstance(docs[0], dict):
                if 'VERSION' in docs[0]:
                    return docs[0]['VERSION']
                if 'version' in docs[0]:
                    return docs[0]['version']
                return self.PIPJSON_VERSION
            else:
                raise ArgumentError('docs', 'Invalid type {0} for vnm.yml:docs[0]'.format(type(docs[0])))
        elif isinstance(docs, dict):
            return docs.get('version', self.VNMYML_VERSION)

    def getStateVersion(self, docs) -> str:
        if isinstance(docs, list):
            if isinstance(docs[0], int):
                return str(docs[0])
            elif isinstance(docs[0], str):
                return docs[0]
            raise ArgumentError('docs', 'Invalid type {0} for vnm.state:docs[0]'.format(type(docs[0])))
        else:
            raise ArgumentError('docs', 'Invalid type {0} for vnm.state:docs'.format(type(docs)))

    def load(self) -> None:
        self.as_json = False
        data = {}
        statedata = {}
        if os.path.isfile('vnm.yml'):
            with open('vnm.yml', 'r') as f:
                docs = yaml.load_all(f)
                if isinstance(docs, types.GeneratorType):
                    docs = list(docs)
                version = self.getYamlVersion(docs)
                while version in self.yaml_upgrades:
                    print(f'WARNING: Updating vnm.yml to version {version+1}...')
                    docs = self.yaml_upgrades[version](docs)
                    version = self.getYamlVersion(docs)
                #print(repr(docs))
                data = docs[0]
        elif os.path.isfile('vnm.json'):
            self.as_json=True
            with open('vnm.json', 'r') as f:
                data = json.load(f)

        if os.path.isfile('vnm.state'):
            with open('vnm.state', 'r') as f:
                docs = list(yaml.load_all(f))
                version = self.getStateVersion(docs)
                while version in self.state_upgrades:
                    docs = self.state_upgrades[version](docs)
                    version = self.getStateVersion(docs)
                    print(f'WARNING: Updated vnm.state to version {version}...')
                statedata = docs[1]
                self.dev_mode = statedata.get('dev-mode', False)

        self.egginfo = data.get('package-info', {})
        #print(repr(self.egginfo))

        opts = data.get('options', {})
        self.generate_setup = opts.get('generate-setup', False)
        self.generate_requirements = opts.get('generate-requirements', False)

        pkgdata = data.get('packages', {})
        for k, v in pkgdata.items():
            pkg = Package()
            pkg.id = k
            pkg.deserialize(v)
            self.packages[k] = pkg

        pkgdata = data.get('dev-packages', {})
        for k, v in pkgdata.items():
            pkg = Package()
            pkg.id = k
            pkg.deserialize(v)
            self.dev_packages[k] = pkg

    def get_packages(self) -> Dict[str, Package]:
        o = self.packages.copy()
        if self.dev_mode:
            o.update(self.dev_packages)
        return o

    def get_all_packages(self) -> Dict[str, Package]:
        return {**self.packages, **self.dev_packages}

    def _serialize_pkg_dict(self, d):
        o = collections.OrderedDict()
        for k in sorted(d.keys()):
            o[k]=d[k].serialize()
        return dict(o)

    def import_setup(self, filename) -> None:
        from setuptools.config import read_configuration
        self.egginfo = dict(read_configuration(str(filename), ignore_option_errors=True))
        if 'requires' in self.egginfo['metadata']:
            for v in self.egginfo['metadata']['requires']:
                pkg = Package(v)
                self.packages[pkg.id] = pkg
        if 'options' in self.egginfo:
            if 'install_requires' in self.egginfo['options']:
                for v in self.egginfo['options']['install_requires']:
                    pkg = Package(v)
                    self.packages[pkg.id] = pkg


    def update_setup(self, args, release_pkgs, all_pkgs, pkgs) -> None:
        cfg = {}
        def _fix(d: dict) -> dict:
            o = {}
            for _k, _v in d.items():
                k = _k.replace('-', '_')
                v = _v
                if isinstance(_v, collections.OrderedDict):
                    v = _fix(_v)
                o[k] = v
            return o

        cfg = _fix(self.egginfo)

        if 'options' not in cfg:
            cfg['options'] = {}
        cfg['options']['install_requires'] = ''.join(['\n'+pkg.toRequirement() for pkg in sorted(pkgs.values(), key=lambda p: p.priority) if pkg.id.lower() in release_pkgs])

        def _section(section, handlers) -> None:
            for option, handler in handlers.items():
                if section in cfg and option in cfg[section]:
                    cfg[section][option] = handler(cfg[section][option])

        def _iniList(v) -> Any:
            if isinstance(v, list):
                return ''.join(['\n'+x for x in v])
            return v

        def _iniBool(v) -> Any:
            if isinstance(v, bool):
                return 'True' if v else 'False'
            return v

        def _iniDict(v) -> Any:
            if isinstance(v, dict):
                return ''.join([f'\n{k}={v}' for k,v in v.items()])
            return v

        def _asSection(origpath, section, parser=None) -> None:
            if isinstance(origpath, str):
                origpath = origpath.split('.')
            parser = parser or (lambda x: x)
            origpath = list(origpath)
            k = origpath[0]
            if k not in cfg:
                return None
            origpath=origpath[1:]
            cval = cfg[k]
            pval = None
            lk = None
            if len(origpath):
                for k in origpath:
                    if k not in cfg:
                        return None
                    pval = cval
                    lk = k
                    cval = cval[k]
            if hasattr(cval, 'items'):
                for option, value in cval.items():
                    cfg[section][option] = parser(value)
            if pval is not None and lk is not None:
                del pval[lk]

        def _toSection(newsection, parser=None):
            parser = parser or (lambda x: x)
            def _handler(v) -> Any:
                assert isinstance(v, dict)
                if newsection not in cfg:
                    cfg[newsection] = {}
                for option,value in v.items():
                    cfg[newsection][option] = parser(value)
            return _handler

        # https://github.com/pypa/setuptools/blob/30cf7823c7acd8ba5503ed3fdc7dc9cb28800880/setuptools/config.py#L511
        _section('metadata', {
            'platforms': _iniList,
            'keywords': _iniList,
            'provides': _iniList,
            'obsoletes': _iniList,
            'classifiers': _iniList,
            'license': _iniList,
            'license_files': _iniList,
            'project_urls': _iniDict,
        })

        _section('options', {
            'zip_safe': _iniBool,
            'use_2to3': _iniBool,
            'include_package_data': _iniBool,
            'package_dir': _iniDict,
            'use_2to3_fixers': _iniList,
            'use_2to3_exclude_fixers': _iniList,
            'convert_2to3_doctests': _iniList,
            'scripts': _iniList,
            'eager_resources': _iniList,
            'dependency_links': _iniList,
            'namespace_packages': _iniList,
            'install_requires': _iniList,
            'setup_requires': _iniList,
            'tests_require': _iniList,
            'py_modules': _iniList,
            'python_requires': _iniList,
            'entry_points': _toSection('options.entry_points', parser=_iniList)
        })

        filename = 'setup.cfg'
        opts = configparser.RawConfigParser()
        #opts.read([filename])
        for section, options in cfg.items():
            if options is None:
                opts.remove_section(section)
            else:
                if not opts.has_section(section):
                    log.debug("Adding new section [%s] to %s", section, filename)
                    opts.add_section(section)
                for option, value in options.items():
                    if value is None:
                        log.debug(
                            "Deleting %s.%s from %s",
                            section, option, filename
                        )
                        opts.remove_option(section, option)
                        if not opts.options(section):
                            log.info("Deleting empty [%s] section from %s",
                                     section, filename)
                            opts.remove_section(section)
                    else:
                        log.debug(
                            "Setting %s.%s to %r in %s",
                            section, option, value, filename
                        )
                        opts.set(section, option, value)
        with open(filename, 'w') as f:
            f.write('# @generated by vnm (see vnm.yml:/package-info)\n')
            opts.write(f)

    def saveVNM(self, dry_run: bool=False) -> None:
        if self.as_json:
            data = {
                'version': self.PIPJSON_VERSION,
                'options': {
                    'generate-setup': self.generate_setup,
                    'generate-requirements': self.generate_requirements,
                },
            }
            if len(self.egginfo) > 0:
                data['package-info'] = self.egginfo
            if len(self.packages) > 0:
                data['packages'] = self._serialize_pkg_dict(self.packages)
            if len(self.dev_packages) > 0:
                data['dev-packages'] = self._serialize_pkg_dict(self.dev_packages)
            with open('vnm.new.json' if dry_run else 'vnm.json', 'w') as f:
                json.dump(data, f, indent=2)
        else:
            data = {
                'version': self.VNMYML_VERSION,
                'options': {
                    'generate-setup': self.generate_setup,
                    'generate-requirements': self.generate_requirements,
                },
            }
            if len(self.egginfo) > 0:
                data['package-info'] = self.egginfo
            if len(self.packages) > 0:
                data['packages'] = self._serialize_pkg_dict(self.packages)
            if len(self.dev_packages) > 0:
                data['dev-packages'] = self._serialize_pkg_dict(self.dev_packages)
            with open('vnm.new.yml' if dry_run else 'vnm.yml', 'w') as f:
                f.write('# Generated by vnm.\n')
                yaml.dump(data, f)

    def saveState(self, dry_run: bool=False) -> None:
        data={}
        if self.dev_mode:
            data['dev-mode']=True
        # Mostly for debugging purposes.
        if self.as_json:
            data['as-json']=True
        with open(self.STATE_FILENAME + ('.new' if dry_run else ''), 'w') as f:
            f.write(f'# vnm state file version {self.STATE_VERSION}\n')
            f.write('# @GENERATED automatically by vnm.\n')
            f.write('# Do NOT edit this file, nor commit it to your VCS.\n')
            f.write('###################################################\n')
            f.write(f'{self.STATE_VERSION!r}\n')
            f.write(f'---\n')
            yaml.dump(data, f)
