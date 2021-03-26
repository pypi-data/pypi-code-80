#  load configuration from treedb.ini

import configparser
import logging
import os

from . import _globals
from . import _tools

__all__ = ['get_default_root',
           'configure']

ROOT_OPTION = ('glottolog', 'repo_root')

ENGINE_OPTION = ('treedb', 'engine')

NOT_SET = object()


log = logging.getLogger(__name__)


def get_default_root(*, env_var,
                     config_path=_globals.CONFIG,
                     fallback=_globals.DEFAULT_ROOT):
    """Return default root from environment variable, config, or fallback."""
    root = os.getenv(env_var)

    if root is None:
        log.debug('get %r from optional config file %r', ROOT_OPTION, config_path)
        cfg = ConfigParser.from_file(config_path, default_repo_root=fallback)
        root = cfg.get(*ROOT_OPTION)

    return root


class ConfigParser(configparser.ConfigParser):

    @classmethod
    def from_file(cls, path, *, required=False, default_repo_root):
        path = _tools.path_from_filename(path).resolve()

        defaults = {'here': path.parent.as_posix()}
        inst = cls(defaults=defaults)
        inst.set_default_repo_root(default_repo_root)

        found = inst.read([path])
        if found:
            log.debug('%s().read() config file(s): %r', cls.__name__, found)
        elif required:
            raise ValueError(f'config file not found: {path!r}')
        else:
            log.debug('no config file(s) found')
        return inst

    def set_default_repo_root(self, repo_root):
        self.add_section(ROOT_OPTION[0])
        self.set(*ROOT_OPTION, repo_root)


def configure(config_path=_globals.CONFIG,
              *, engine=NOT_SET, root=NOT_SET,
              loglevel=None, log_sql: bool = None,
              default_repo_root=_globals.DEFAULT_ROOT):
    """Set root, and engine and configure logging from the given .ini file."""
    log.info('configure from %r', config_path)
    log.debug('default repo root: %r', default_repo_root)

    from . import (logging_,
                   files,
                   backend)

    config_path = _tools.path_from_filename(config_path)
    log.debug('load config file %r', config_path)
    cfg = ConfigParser.from_file(config_path,
                                 required=True,
                                 default_repo_root=default_repo_root)

    log.info('configure logging from %r', config_path)
    logging_.configure_logging_from_file(cfg, level=loglevel, log_sql=log_sql)

    if engine is NOT_SET:
        engine = cfg.get(*ENGINE_OPTION, fallback=None)
    if engine is not None:
        engine = _tools.path_from_filename(engine)
        if not engine.is_absolute():
            engine = config_path.parent / engine
    backend.set_engine(engine)

    if root is NOT_SET:
        root = cfg.get(*ROOT_OPTION)
    root = _tools.path_from_filename(root)
    if not root.is_absolute():
        root = config_path.parent / root
    files.set_root(root)
