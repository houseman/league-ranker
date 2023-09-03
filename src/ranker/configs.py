"""
Configuration container for League Ranker.

> **Important**
> There is precedence to these configuration methods. From highest to lowest priority:
> 1. Command line options (supersede)
> 2. Environment variables (supersede)
> 3. Configuration file
"""
from __future__ import annotations

import logging
import os
import os.path
import typing as t
from pathlib import Path

import yaml

from .errors import ConfigurationError

logger = logging.getLogger(__name__)


S = t.TypeVar("S", bound=bool | int | str)
P = t.ParamSpec("P")
KeyValuePairs: t.TypeAlias = dict[str, S]


class LeagueRankerConfig:
    """Configuration container for League Ranker."""

    _prefix = "RANKER"
    _config_filename = "league-ranker.yaml"
    _config_dirs = [
        os.getcwd(),  # Current working directory
        os.path.expanduser("~/.ranker/"),  # ${HOME}/.ranker/
        # Ranker base directory
        Path(__file__).absolute().parent.parent.absolute().as_posix(),
    ]
    _truthey = [1, "1", True, "True", "true"]  # Values that should evaluate to `True`

    def __init__(self) -> None:
        self._data: KeyValuePairs = {}

        self._load_from_env()
        self._load_from_file(self._find_config_path())
        logger.info(f"Config {self._data} at init")

    @classmethod
    def create(cls, init: KeyValuePairs | None = None) -> LeagueRankerConfig:
        """
        A static method to be used to create the first Singleton instance.

        A dictionary containing key:value pairs may be given as an `init` parameter.
        These pairs will be injected into the environment before creating the instance.
        """
        if init is not None:
            for k, v in init.items():
                os.environ[cls.env_key(k)] = str(v)

        return cls()

    def has_key(self, key: str) -> bool:
        """Return `True` if the given key has a set value, else `False`."""
        return key in self._data

    def get_str(self, key: str, default: str | None = None) -> str:
        """
        Return a string value for the given key.

        If no value exists for the key, the default value is returned (if provided).
        If no default value is provided, a `ConfigurationError` exception will raise.
        """
        try:
            return str(self._data[key])
        except KeyError:
            if default is not None:
                return default
            raise ConfigurationError(f"Configuration key '{key}' is not set") from None

    def get_int(self, key: str, default: int | None = None) -> int:
        """
        Return an integer value for the given key.

        If no value exists for the key, the default value is returned (if provided).
        If no default value is provided, a `ConfigurationError` exception will raise.
        """
        try:
            return int(self._data[key])
        except KeyError:
            if default is not None:
                return default
            raise ConfigurationError(f"Configuration key '{key}' is not set") from None
        except ValueError:
            raise ConfigurationError(
                f"Configuration key '{key}' value cannot be returned as type 'int'"
            ) from None

    def get_bool(self, key: str, default: bool | None = None) -> bool:
        """
        Return a boolean value for the given key.

        If no value exists for the key, the default value is returned (if provided).
        If no default value is provided, a `ConfigurationError` exception will raise.
        """
        try:
            return self._data[key] in self._truthey
        except KeyError:
            if default is not None:
                return default
            raise ConfigurationError(f"Configuration key '{key}' is not set") from None

    def _load_from_file(self, path: str) -> None:
        """Load configurations from a YAML file located at the given path."""
        logger.info(f"Read config from file {path}")

        try:
            with open(path, encoding="locale") as file:
                self._merge(yaml.safe_load(file).get("config", {}))
        except FileNotFoundError as e:
            raise ConfigurationError(f"Could not read from file '{path}'") from e

    @classmethod
    def env_key(cls, key: str) -> str:
        """Return the prefixed environment variable name for the given key name."""
        prefix = cls._prefix.upper() + "_"

        return prefix + key.upper()

    def _load_from_env(self) -> None:
        """Load values from environment that match `sel._prefix."""
        prefix = self._prefix.upper() + "_"

        logger.info(f"Read config from environment (prefix is '{prefix}')")

        self._merge(
            {
                str(k).upper().replace(prefix, "").lower(): v
                for k, v in os.environ.items()
                if str(k).upper().startswith(prefix)
            }
        )

    def _merge(self, pairs: KeyValuePairs, mutate: bool = False) -> None:
        """Merge the given config key:value pairs into the internal config store."""
        for k, v in pairs.items():
            if mutate or k not in self._data:
                self._data[k] = v
                logger.debug(f"Added config key {k}: {v}")
            else:
                logger.debug(f"Config key '{k}' exists ('{self._data[k]}')")

    def _find_config_path(self) -> str:
        """Look for a config file path in pre-defined locations."""
        if self.has_key("config_path"):
            return self.get_str("config_path")

        # If this is not set in environment, then look for it in `_config_dirs`
        for dir in self._config_dirs:
            path = os.path.join(dir, self._config_filename)
            logger.debug(f"Looking for config file {path}")

            if os.path.isfile(path):
                self._merge({"config_path": path})

                return self.get_str("config_path")

        raise ConfigurationError(f"No configuration file found in {self._config_dirs}")
