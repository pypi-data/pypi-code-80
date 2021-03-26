"""Shared parent class for Tap, Target (future), and Transform (future)."""

import abc
from collections import OrderedDict
import json
import logging
import os
from types import MappingProxyType
from typing import Dict, List, Mapping, Optional, Tuple, Any, Union, cast
from jsonschema import ValidationError, SchemaError, Draft4Validator
from pathlib import PurePath

from singer_sdk.helpers.classproperty import classproperty
from singer_sdk.helpers.util import read_json_file
from singer_sdk.helpers.secrets import is_common_secret_key, SecretString
from singer_sdk.helpers.typing import extend_with_default

import click

SDK_PACKAGE_NAME = "singer_sdk"


try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata  # type: ignore


JSONSchemaValidator = extend_with_default(Draft4Validator)


class PluginBase(metaclass=abc.ABCMeta):
    """Abstract base class for taps."""

    name: str = "sample-plugin-name"
    config_jsonschema: Optional[dict] = None
    protected_config_keys: List[str] = []

    _config: dict

    @classproperty
    # @classmethod
    def logger(cls) -> logging.Logger:
        """Get logger."""
        return logging.getLogger(cls.name)

    # Constructor

    def __init__(
        self,
        config: Optional[Union[dict, PurePath, str, List[Union[PurePath, str]]]] = None,
        parse_env_config: bool = False,
    ) -> None:
        """Initialize the tap or target.

        - `config` may be one or more paths, either as str or PurePath objects, or
        it can be a predetermined config dict.
        - `parse_env_config` - True to parse settings from env vars.
        """
        if not config:
            config_dict = {}
        elif isinstance(config, str) or isinstance(config, PurePath):
            config_dict = read_json_file(config)
        elif isinstance(config, list):
            config_dict = {}
            for config_path in config:
                # Read each config file sequentially. Settings from files later in the
                # list will override those of earlier ones.
                config_dict.update(read_json_file(config_path))
        elif isinstance(config, dict):
            config_dict = config
        else:
            raise ValueError(f"Error parsing config of type '{type(config).__name__}'.")
        if parse_env_config:
            self.logger.info("Parsing env var for settings config...")
            config_dict.update(self.get_env_var_config())
        else:
            self.logger.info("Skipping parse of env var settings...")
        for k, v in config_dict.items():
            if self.is_secret_config(k):
                config_dict[k] = SecretString(v)
        self._config = config_dict
        self._validate_config()

    @property
    def capabilities(self) -> List[str]:
        """Return a list of supported capabilities."""
        return []

    @classmethod
    def get_env_var_config(cls) -> Dict[str, Any]:
        """Return any config specified in environment variables.

        Variables must match the convention "PLUGIN_NAME_setting_name",
        with dashes converted to underscores, the plugin name converted to all
        caps, and the setting name in same-case as specified in settings config.
        """
        result: Dict[str, Any] = {}
        plugin_env_prefix = f"{cls.name.upper().replace('-', '_')}_"
        for config_key in cls.config_jsonschema["properties"].keys():
            env_var_name = plugin_env_prefix + config_key
            if env_var_name in os.environ:
                env_var_value = os.environ[env_var_name]
                config_key = env_var_name.split(plugin_env_prefix)[1]
                cls.logger.info(
                    f"Parsing '{config_key}' config from env variable '{env_var_name}'."
                )
                if env_var_value[0] == "[" and env_var_value[-1] == "]":
                    result[config_key] = (
                        env_var_value.lstrip("[").rstrip("]").split(",")
                    )
                else:
                    result[config_key] = env_var_value
        return result

    # Core plugin metadata:

    @classproperty
    # @classmethod
    def plugin_version(cls) -> str:
        """Return the package version number."""
        try:
            version = metadata.version(cls.name)
        except metadata.PackageNotFoundError:
            version = "[could not be detected]"
        return version

    @classproperty
    # @classmethod
    def sdk_version(cls) -> str:
        """Return the package version number."""
        try:
            version = metadata.version(SDK_PACKAGE_NAME)
        except metadata.PackageNotFoundError:
            version = "[could not be detected]"
        return version

    # Abstract methods:

    @property
    def state(self) -> dict:
        """Return the state dict for the plugin."""
        raise NotImplementedError()

    @property
    def input_catalog(self) -> Optional[dict]:
        """Return the catalog dictionary input, or None if not provided."""
        raise NotImplementedError()

    # Core plugin config:

    @property
    def config(self) -> Mapping[str, Any]:
        """Return a frozen (read-only) config dictionary map."""
        return cast(Dict, MappingProxyType(self._config))

    def is_secret_config(self, config_key: str) -> bool:
        """Return true if a config value should be treated as a secret.

        This avoids accidental printing to logs, and it prevents rendering the secrets
        in jinja templating functions.
        """
        return (
            is_common_secret_key(config_key) or config_key in self.protected_config_keys
        )

    def _validate_config(
        self, raise_errors: bool = True, warnings_as_errors: bool = False
    ) -> Tuple[List[str], List[str]]:
        """Return a tuple: (warnings: List[str], errors: List[str])."""
        warnings: List[str] = []
        errors: List[str] = []
        if self.config_jsonschema:
            try:
                self.logger.debug(
                    f"Validating config using jsonschema: {self.config_jsonschema}"
                )
                validator = JSONSchemaValidator(self.config_jsonschema)
                validator.validate(self._config)
            except (ValidationError, SchemaError) as ex:
                errors.append(str(ex))
        if errors:
            summary = (
                f"Config validation failed: {f'; '.join(errors)}\n"
                f"JSONSchema was: {self.config_jsonschema}"
            )
            if raise_errors:
                raise RuntimeError(summary)
        else:
            summary = (
                f"Config validation passed with 0 errors and {len(warnings)} warnings."
            )
            for warning in warnings:
                summary += f"\n{warning}"
        if warnings_as_errors and raise_errors and warnings:
            raise RuntimeError(
                f"One or more warnings ocurred during validation: {warnings}"
            )
        self.logger.info(summary)
        return warnings, errors

    @classmethod
    def print_version(cls) -> None:
        """Print help text for the tap."""
        print(f"{cls.name} v{cls.plugin_version}")

    @classmethod
    def print_about(cls, format: Optional[str]) -> None:
        """Print capabilities and other tap metadata."""
        info = OrderedDict[str, Any]()
        info["name"] = cls.name
        info["version"] = cls.plugin_version
        info["sdk_version"] = cls.sdk_version
        info["capabilities"] = cls.capabilities
        info["settings"] = cls.config_jsonschema
        if format == "json":
            print(json.dumps(info, indent=2))
        else:
            formatted = "\n".join([f"{k.title()}: {v}" for k, v in info])
            print(formatted)

    @classmethod
    @click.command()
    def cli(cls):
        """Handle command line execution."""
        pass
