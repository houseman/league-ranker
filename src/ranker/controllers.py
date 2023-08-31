"""
Controller classes contain business and flow logic.

The `LeagueRankController` class follows teh builder pattern
"""

from __future__ import annotations

import typing as t

from .factories import LogTableFactory
from .parsers import LeagueRankerParser
from .readers import InputDataReader
from .stats import StatsCounter

if t.TYPE_CHECKING:
    import io

    from . import models as m
    from .configs import LeagueRankerConfig


class LeagueRankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(self, config: LeagueRankerConfig) -> None:
        self._config = config
        self._factory = LogTableFactory()
        self._stats = StatsCounter()

    def read(self, stream: io.TextIOWrapper) -> t.Self:
        """Read data from an input stream."""
        self._reader = InputDataReader()
        self._reader.load_from_stream(stream=stream)

        return self

    def parse(self) -> t.Self:
        """Invoke the parser."""
        self._parser = LeagueRankerParser(
            reader=self._reader,
            stats=self._stats,
            strict=self._config.is_strict_mode,
        )
        self._input_model = self._parser.parse()

        return self

    def build(self) -> t.Self:
        """Invoke the factory build."""
        self._table = self._factory.build(input=self._input_model)

        return self

    def sort(self) -> m.LogTableModel:
        """Sort and return results."""
        self._table.sort()

        return self._table

    def dump(self) -> None:
        """Dump the raw input data to output."""
        print(self._parser.reader.data)

    @property
    def stats(self) -> StatsCounter:
        """Return controller stats."""
        return self._stats
