"""
snapsheets.config.py
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import toml
import yaml
from deprecated import deprecated

_config = "Run set_default_config() first"


@deprecated(version="0.2.3", reason="Will be removed.")
def get_config() -> Any:
    """
    Return config

    Returns
    -------
    dict
        current config
    """
    return _config


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def set_config(fname: str) -> Any:
    """
    Set config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        config
    """
    with open(fname, "r") as f:
        config = yaml.safe_load(f)
    return config


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def set_default_config() -> Any:
    """
    Set default config

    Returns
    -------
    dict
        config
    """
    here = Path(__file__).resolve().parent
    fname = str(here / "config.yml")
    return set_config(fname)


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.load_config()",
)
def add_config(fname: str) -> Any:
    """
    Update config

    Parameters
    ----------
    fname : str
        filename of config in yaml format

    Returns
    -------
    dict
        updated config
    """
    config = get_config()
    add = set_config(fname)
    config.update(add)
    return config


def show_config() -> None:
    """
    Show config
    """
    import pprint

    config = get_config()
    pprint.pprint(config)
    return


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.volumes()",
)
def volumes() -> Any:
    """
    List volumes

    Returns
    -------
    dict
        list of volumes
    """
    config = get_config()
    return config.get("volumes")


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.options()",
)
def options() -> Any:
    """
    List options

    Returns
    -------
    dict
        list of options
    """
    config = get_config()
    return config.get("options")


@deprecated(
    version="0.2.3",
    reason="Will be removed. Testing migration to config.Config.sheets()",
)
def sheets() -> Any:
    """
    List spreadsheets

    Returns
    -------
    list
        list of spreadsheets
    """
    config = get_config()
    return list(config.get("sheets").keys())


@deprecated(
    version="0.2.2",
    reason="Will be removed. Testing migration to config.Config.sheet(name)",
)
def sheet(name: str) -> Any:
    """
    Show spreadsheet info

    Parameters
    ----------
    name : str
        name of spreadsheet

    Returns
    -------
    dict
        spreadsheet info
    """
    config = get_config()
    return config.get("sheets").get(name)


# Set default config
_config = set_default_config()


@dataclass
class Config:
    path: str = ""

    def get_fnames(self, fmt: str) -> List[Path]:
        p = Path(self.path)
        fnames = sorted(p.glob(fmt))
        return fnames

    def load_yaml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.yml")
        for fname in fnames:
            with open(fname) as f:
                c = yaml.safe_load(f)
                config.update(c)
        return config

    def load_toml(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        fnames = self.get_fnames("*.toml")
        for fname in fnames:
            c = toml.load(fname)
            config.update(c)
        return config

    def load_config(self) -> Dict[Any, Any]:
        config: Dict[Any, Any] = {}
        c = self.load_yaml()
        config.update(c)
        c = self.load_toml()
        config.update(c)
        self.config = config
        return config

    def sections(self) -> List[str]:
        return list(self.config.keys())

    def volumes(self) -> Optional[str]:
        return self.config.get("volumes")

    def options(self) -> Optional[str]:
        return self.config.get("options")

    def datefmt(self) -> Optional[str]:
        return self.config.get("datefmt")

    def sheets(self) -> Any:
        return self.config.get("sheets")

    def sheet_names(self) -> Any:
        sheets = self.sheets()
        names = sorted(sheets.keys())
        return names

    def sheet(self, name: str) -> Any:
        sheets = self.sheets()
        return sheets.get(name)
