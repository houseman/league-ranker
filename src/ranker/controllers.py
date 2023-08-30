"""Controller classes contain business and flow logic."""

from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from .configs import BaseConfig
    from .parsers import BaseParser


class AbstractController(ABC):
    """Abstract Controller class defines minimum required Controller functionality."""

    @abstractmethod
    def __init__(self, parser: BaseParser, config: BaseConfig) -> None:
        pass

    @abstractmethod
    def parse(self) -> None:
        """Controllers must implement a parse method."""
        pass


class BaseController(AbstractController):
    """Implements base functionality for Controller classes."""

    def __init__(self, parser: BaseParser, config: BaseConfig) -> None:
        self._parser = parser
        self._config = config

    def parse(self) -> None:
        """Invoke the parser."""
        self._parser.parse()


class LeagueRankController(BaseController):
    """Controller class contains logic for the League Ranker."""

    def dump(self) -> None:
        """Dump the raw input data to output."""
        print(self._parser.reader.data)
