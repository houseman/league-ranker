"""Controller classes contain business and flow logic."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from . import models as m
    from .configs import LeagueRankerConfig
    from .factories import LogTableFactory
    from .parsers import LeagueRankerParser


class LeagueRankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(
        self,
        parser: LeagueRankerParser,
        config: LeagueRankerConfig,
        factory: LogTableFactory,
    ) -> None:
        self._parser = parser
        self._config = config
        self._factory = factory

    def parse(self) -> m.InputMatchResultsModel:
        """Invoke the parser."""
        return self._parser.parse()

    def build(self, source: m.InputMatchResultsModel) -> m.LogTableModel:
        """Invoke the factory build."""
        return self._factory.build(source)

    def dump(self) -> None:
        """Dump the raw input data to output."""
        print(self._parser.reader.data)
