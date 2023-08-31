"""Controller classes contain business and flow logic."""

from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    from .configs import BaseConfig
    from .factories import BaseFactory
    from .models import BaseModel
    from .parsers import BaseParser


class AbstractController(ABC):
    """Abstract Controller class defines minimum required Controller functionality."""

    @abstractmethod
    def __init__(
        self, parser: BaseParser, config: BaseConfig, factory: BaseFactory
    ) -> None:
        pass

    @abstractmethod
    def parse(self) -> BaseModel:
        """Controllers must implement a parse method."""
        pass

    @abstractmethod
    def build(self, source: BaseModel) -> BaseModel:
        """Controllers must implement a build method."""
        pass


class BaseController(AbstractController):
    """Implements base functionality for Controller classes."""

    def __init__(
        self, parser: BaseParser, config: BaseConfig, factory: BaseFactory
    ) -> None:
        self._parser = parser
        self._config = config
        self._factory = factory

    def parse(self) -> BaseModel:
        """Invoke the parser."""
        return self._parser.parse()

    def build(self, source: BaseModel) -> BaseModel:
        """Invoke the factory build."""
        return self._factory.build(source)


class LeagueRankController(BaseController):
    """Controller class contains logic for the League Ranker."""

    def dump(self) -> None:
        """Dump the raw input data to output."""
        print(self._parser.reader.data)
