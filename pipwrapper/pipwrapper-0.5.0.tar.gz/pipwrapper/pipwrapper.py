#!/usr/bin/env python3
"""


Copyright::
    
    +===================================================+
    |                 © 2021 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |     Python PIP Wrapper Library                    |
    |     License: X11/MIT                              |
    |     Repo: https://github.com/Privex/pipwrapper    |
    |                                                   |
    |     Core Developer(s):                            |
    |                                                   |
    |       (+)  Chris (@someguy123) [Privex]           |
    |                                                   |
    +===================================================+
    
    Python PIP Wrapper (PyPi Wrapper) - A simple, dependency-free library for using PIP via wrapping the CLI utility (python3.x -m pip ARGS)
    Copyright (c) 2021    Privex Inc. ( https://www.privex.io )


"""
import sys
import subprocess
import logging
from os import getenv as env
from subprocess import PIPE, STDOUT
from typing import Any, Callable, List, NamedTuple, Optional, Union

VERSION = '0.5.0'

PIP_LOG_LEVEL = env('PIP_LOG_LEVEL', 'WARNING').upper()

log = logging.getLogger('pipwrapper')
log.setLevel(logging.DEBUG)

_hd = logging.StreamHandler(sys.stderr)
_hd.setLevel(logging.getLevelName(PIP_LOG_LEVEL))
log.addHandler(_hd)

__all__ = ['ProcResult', 'Pip', 'PIP_LOG_LEVEL', 'VERSION']


def err(*args, file=sys.stderr, **kwargs):
    return print(*args, file=file, **kwargs)


class ProcResult(NamedTuple):
    stdout: Optional[bytes] = None
    stderr: Optional[bytes] = None
    retcode: int = 0
    

def stringify(d, encoding='utf-8', fail_none=False, fail_bool=False) -> str:
    if d is None:
        if fail_none: raise ValueError("Passed object to stringify is None and fail_none is True! Can't stringify None.")
        return ''
    if isinstance(d, bool):
        if fail_bool: raise ValueError(f"Passed object to stringify is boolean ('{d}') and fail_bool is True! Can't stringify boolean.")
        return str(d)
    if isinstance(d, str): return d
    if isinstance(d, (bytes, bytearray)): return d.decode(encoding)
    return str(d)


class Pip(object):
    """
    Python PIP Wrapper (PyPi Wrapper) - A simple, dependency-free library for using PIP via wrapping the CLI utility
        Copyright (c) 2021      Privex Inc. ( https://www.privex.io )
        License:  X11/MIT       Repo: https://github.com/Privex/pipwrapper
    
    
    **Example usage**
    
    Using :meth:`.auto_install` - it will check for any required packages that aren't already installed, and then
    automatically install any specified packages which are missing::
    
        >>> xrs = Pip.auto_install('privex-helpers', 'pypng', 'cairosvg', 'humanize')
         [!!!] Installing missing packages: ['privex-helpers', 'pypng', 'cairosvg', 'humanize']
        >>> xrs.retcode
        0
        >>> print(xrs.stdout.decode('utf-8'))
        Collecting privex-helpers
          Using cached privex_helpers-3.2.1-py3-none-any.whl (231 kB)
        Processing /Users/chris/Library/Caches/pip/wheels/28/dd/ea/756ac2cb38f4e73f04a756fb3b4650e5f5dcd019a641098959/pypng-0.0.20-py3-none-any.whl
        Collecting cairosvg
          Using cached CairoSVG-2.5.2-py3-none-any.whl (45 kB)
        Collecting humanize
          Using cached humanize-3.3.0-py3-none-any.whl (70 kB)
        .............
        
        Installing collected packages: privex-helpers, pypng, cairosvg, humanize
        Successfully installed cairosvg-2.5.2 humanize-3.3.0 privex-helpers-3.2.1 pypng-0.0.20
        
        
    Using :meth:`.install` , you can install/upgrade one or more Python packages, and collect pip's output / return code::
    
        >>> Pip.install('pillow')
        Out[14]: ProcResult(
            stdout=b"Collecting pillow\n  Using cached Pillow-8.1.2-cp39-cp39-macosx_10_10_x86_64.whl (2.2 MB)\nInstalling
                     collected packages: pillow\nSuccessfully installed pillow-8.1.2\nWARNING: You are using pip version 20.2.3; however,
                     version 21.0.1 is available.\nYou should consider upgrading via the  '/tmp/tmp.awnu6YYn/venv/bin/python3 -m pip
                     install --upgrade pip' command.\n",
            stderr=None,
            retcode=0
        )
        
        >>> res = Pip.install('privex-asdf-does-not-exist')
        >>> print(res.retcode)
        1
        >>> print(res.stdout.decode('utf-8'))
        ERROR: Could not find a version that satisfies the requirement privex-asdf-does-not-exist (from versions: none)
        ERROR: No matching distribution found for privex-asdf-does-not-exist
        WARNING: You are using pip version 20.2.3; however, version 21.0.1 is available.
        You should consider upgrading via the '/tmp/tmp.awnu6YYn/venv/bin/python3 -m pip install --upgrade pip' command.
    
    
    By passing ``output=True`` to most methods such as :meth:`.install`, :meth:`.uninstall`, :meth:`.auto_install` etc. -
    the argument will be passed through down to :meth:`.call`.
    
    The kwarg ``output=True`` acts as a shortcut for ``stdout=None, stderr=None``, and causes both the ``stdout`` and ``stderr`` of the
    command being ran to bypass :class:`subprocess.Popen` 's capturing, instead, they'll both be piped into the current script's
    stdout/stderr in realtime as they execute::
    
        >>> Pip.install('pillow', output=True)
        Requirement already up-to-date: pillow in ./venv/lib/python3.9/site-packages (8.1.2)
        WARNING: You are using pip version 20.2.3; however, version 21.0.1 is available.
        You should consider upgrading via the '/tmp/tmp.awnu6YYn/venv/bin/python3 -m pip install --upgrade pip' command.
        Out[12]: ProcResult(stdout=None, stderr=None, retcode=0)
        
        >>> Pip.uninstall('pillow', output=True)
        Found existing installation: Pillow 8.1.2
        Uninstalling Pillow-8.1.2:
          Successfully uninstalled Pillow-8.1.2
        Out[13]: ProcResult(stdout=None, stderr=None, retcode=0)
    
    
    Copyright::
        
        +===================================================+
        |                 © 2021 Privex Inc.                |
        |               https://www.privex.io               |
        +===================================================+
        |                                                   |
        |     Python PIP Wrapper Library                    |
        |     License: X11/MIT                              |
        |     Repo: https://github.com/Privex/pipwrapper    |
        |                                                   |
        |     Core Developer(s):                            |
        |                                                   |
        |       (+)  Chris (@someguy123) [Privex]           |
        |                                                   |
        +===================================================+
        
        Python PIP Wrapper (PyPi Wrapper) - A simple, dependency-free library for using PIP via wrapping the CLI utility
        Copyright (c) 2021    Privex Inc. ( https://www.privex.io )
    
        
    """
    PYEXE: str = sys.executable
    PIP: List[str] = [PYEXE, '-m', 'pip']
    QUIET: bool = False
    VERSION: str = VERSION
    
    def __init__(self):
        pass
    
    @classmethod
    def call(cls, *args, write=None, output=False, comm_timeout=30.0, **kwargs) -> ProcResult:
        """
        This is the lower level method which main command methods use to call ``pip`` with whichever
        arguments they use, along with handling advanced settings such as ``stdin`` / ``stdout`` / ``stderr``
        for controlling how/if each file descriptor is captured, ``write`` which allows piping arbitrary bytes
        into the stdin of the command being executed, and many others.
        
        Generally you should use a high level wrapper method such as :meth:`.install` / :meth:`.uninstall` / :meth:`.auto_install`
        rather than this method ( :meth:`.call` ) - unless the pip sub-command you need to call, isn't yet implemented as a
        command wrapper method.
        
        Example usage::
            
            >>> res = Pip.call('install', '-U', 'privex-helpers', 'django', 'pypng')
            >>> res.retcode
            0
            >>> print(res.stdout.decode())
            Requirement already up-to-date: privex-helpers in ./venv/lib/python3.9/site-packages (3.2.1)
            Collecting django
              Downloading Django-3.1.7-py3-none-any.whl (7.8 MB)
            Requirement already up-to-date: pypng in ./venv/lib/python3.9/site-packages (0.0.20)
            Requirement already satisfied, skipping upgrade: python-dateutil in ./venv/lib/python3.9/site-packages (from privex-helpers) (2.8.1)
            Requirement already satisfied, skipping upgrade: privex-loghelper>=1.0.4 in ./venv/lib/python3.9/site-packages (from privex-helpers) (1.0.6)
            Collecting asgiref<4,>=3.2.10 Using cached asgiref-3.3.1-py3-none-any.whl (19 kB)
            Collecting sqlparse>=0.2.2 Using cached sqlparse-0.4.1-py3-none-any.whl (42 kB)
            Requirement already satisfied, skipping upgrade: pytz in ./venv/lib/python3.9/site-packages (from django) (2021.1)
            Installing collected packages: asgiref, sqlparse, django
            Successfully installed asgiref-3.3.1 django-3.1.7 sqlparse-0.4.1

        :param str args:     Arguments to pass (in order) after ``python3.x -m pip```
        :param bytes|None write:  Optional :class:`.bytes` data to be fed into the command's standard input (stdin)
        :param bool output: (Def: ``False``) When ``True``, forces ``stdin=None,stderr=None`` which results in the process' stdout/err
                            being joined into the current Python application's - i.e. the command's output/err will be printed straight
                            to your Python app's stdout/stderr.
        :param float comm_timeout: Max amount of time to wait for the executed command to finish receiving input and sending us output.
                                   If it takes longer than ``comm_timeout``, it should be killed and an exception will be raised,
        :param kwargs:
        :return:
        """
        if output:
            stdout, stderr, stdin = None, None, kwargs.pop('stdin', PIPE)
        else:
            stdout, stderr, stdin = kwargs.pop('stdout', PIPE), kwargs.pop('stderr', STDOUT), kwargs.pop('stdin', PIPE)
        with Pip._popen(*args, stderr=stderr, stdin=stdin, stdout=stdout, **kwargs) as proc:
            if write is not None:
                res_out, res_err = proc.communicate(write, timeout=comm_timeout)
            else:
                res_out, res_err = proc.communicate(timeout=comm_timeout)
            res_out: bytes
            res_err: bytes
            res = ProcResult(stdout=res_out, stderr=res_err, retcode=proc.returncode)
        return res
    
    @classmethod
    def _popen(cls, *args, stderr=PIPE, stdin=PIPE, stdout=PIPE, **kwargs) -> subprocess.Popen:
        return subprocess.Popen(list(cls.PIP) + list(args), stdout=stdout, stderr=stderr, stdin=stdin, **kwargs)
    
    @classmethod
    def freeze(cls, *args, **kwargs) -> List[str]:
        """Calls ``pip freeze`` and returns the list of packages and their versions in requirements.txt format as a :class:`.list`"""
        procres = cls.call(*args, 'freeze', stderr=PIPE, **kwargs)
        return stringify(procres.stdout).splitlines()
    
    @classmethod
    def installed_pkgs(cls, *args, **kwargs) -> List[str]:
        """Calls :meth:`.freeze` - extracts and returns just the package names as a list, with the version specifiers stripped off"""
        return [p.split('==')[0] for p in cls.freeze(*args, **kwargs)]

    @classmethod
    def install(cls, *pkgs, upgrade=True, **kwargs) -> ProcResult:
        """Calls ``pip install [-U] PKGS`` - by default ``upgrade`` is True, so ``-U`` is passed unless you set ``upgrade=False``"""
        return cls.call('install', '-U', *pkgs, **kwargs) if upgrade else cls.call('install', *pkgs, **kwargs)

    @classmethod
    def uninstall(cls, *pkgs, yes=True, **kwargs) -> ProcResult:
        """Calls ``pip uninstall [-y] PKGS`` - by default ``yes`` is True, so ``-y`` is passed unless you set ``yes=False``"""
        return cls.call('uninstall', '-y', *pkgs, **kwargs) if yes else cls.call('uninstall', *pkgs, **kwargs)
    
    remove = uninstall
    
    @staticmethod
    def pkg_in(pl: str, pklist: list) -> bool:
        """
        Returns ``True`` if the package ``pl`` is present in the package list ``pklist`` - cleans up the pkg name ``pl``
        and converts all items in ``pklist`` to lowercase to ensure reliable matching, even if the case differs
        (e.g. ``Django`` instead of ``django``).
        """
        pklist = [p.lower() for p in pklist]
        pl = Pip._clean_pkg(pl)
        return pl in pklist or pl.replace('-', '_') in pklist or pl.replace('_', '-') in pklist

    @staticmethod
    def _clean_pkg(pkg: str) -> str:
        """
        Cleans package name ``pkg`` by casting to string, removing version specifier (``==`` / ``>=`` etc.) if present, and
        converting to lowercase.
        """
        pkg = str(pkg)
        if '==' in pkg: pkg = pkg.split('==')[0]
        if '>=' in pkg: pkg = pkg.split('>=')[0]
        if '<=' in pkg: pkg = pkg.split('<=')[0]
        if '~=' in pkg: pkg = pkg.split('~=')[0]
        return pkg.lower()

    @classmethod
    def has_pkg(cls, pkg: str) -> Optional[str]:
        """If ``pkg`` is installed, then it's proper name according to ``pip freeze`` will be returned. Otherwise ``None`` is returned."""
        pklist = cls.installed_pkgs()
        # if not cls.pkg_in(pkg, pklist):
        #     return None
        clp = cls._clean_pkg(pkg)
        for p in pklist:
            xlp = cls._clean_pkg(p)
            if pkg == p or clp == xlp: return p
            if pkg.replace('-', '_') in [p, xlp] or pkg.replace('_', '-') in [p, xlp]: return p
            if clp.replace('-', '_') in [p, xlp] or clp.replace('_', '-') in [p, xlp]: return p
        return None

    @classmethod
    def auto_install(cls, *pkgs, upgrade=True, **kwargs) -> Optional[ProcResult]:
        """
        Auto-install specified packages if they aren't already installed.
        
        This is useful for early initialisation of single-file scripts, as well as multi-file projects - for automatic
        installation of dependencies from PyPi, without having to explain to the user how to install them.
        
        Example::
        
            >>> Pip.auto_install('django', 'privex-helpers', 'mysqlclient', 'pillow')
        
        :param str pkgs:      Names of packages to check if they're installed, and to auto-install if not already installed.
        :param bool upgrade:  Whether or not to pass ``-U`` to ``pip install`` when auto-installing missing packages.
        :param Any kwargs:    Anything which isn't consumed by this method, will be passed down to :meth:`.install` / :meth:`.call`
        :keyword bool quiet:  (Def: ``False``) When set to ``True``, disables the log / print statements in this method.
        
        :return ProcResult install_log:  The output from ``pip install PKGS`` as a :class:`.ProcResult` named tuple object.
        :return None none:               If no packages were missing (i.e. none were auto-installed), then ``None`` will be returned.
        """
        quiet = kwargs.pop('quiet', cls.QUIET)
        pklist, misspkgs = [p.lower() for p in cls.installed_pkgs()], []
        for p in pkgs:
            pl = cls._clean_pkg(p)
            if cls.pkg_in(p, pklist):
                if not quiet: log.debug(f" [+++] Package {pl!r} ( {p!r} ) already installed. Skipping :)")
                continue
            if not quiet: log.info(f" [!!!] Package {pl!r} ( {p!r} ) not installed. Added to missing packages list for installation.")
            misspkgs.append(p)
        if len(misspkgs) > 0:
            if not quiet: print(f" [!!!] Installing missing packages: {misspkgs}", file=sys.stderr)
            return cls.install(*misspkgs, upgrade=upgrade, **kwargs)
        if not quiet: log.debug(f" [+++] All requested packages appear to already be installed. No need to install any missing packages.")
        return None

    def __getattr__(self, item) -> Union[Any, Callable[..., ProcResult]]:
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            pass
        
        try:
            def _proxy(*args, **kwargs):
                return self.call(item, *args, **kwargs)
            return _proxy
        except Exception as e:
            raise e

    def __enter__(self) -> "Pip": return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass
    
    async def __aenter__(self) -> "Pip": return self
    async def __aexit__(self, exc_type, exc_val, exc_tb): pass


