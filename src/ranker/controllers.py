"""
Controller classes contain business and flow logic.

The `LeagueRankController` class follows teh builder pattern
"""

from __future__ import annotations

import typing as t

from .factories import LogTableFactory
from .parsers import LeagueRankerParser
from .stats import StatsCounter

if t.TYPE_CHECKING:
    from . import models as m
    from .configs import LeagueRankerConfig
    from .requests import CreateLogTableRequest


class LeagueRankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(self, config: LeagueRankerConfig) -> None:
        self._config = config
        self._factory = LogTableFactory()
        self._stats = StatsCounter()
        self._parser = LeagueRankerParser(stats=self._stats)

    def create_log_table(
        self,
        request: CreateLogTableRequest,
    ) -> m.RankingTableModel:
        """Create an return a League Log Table."""
        parsed_data = self.parse(data=request.data)
        table = self.build(data=parsed_data)
        response = self.sort(table=table)

        return response

    def parse(self, data: str) -> m.FixtureListModel:
        """Invoke the parser."""
        return self._parser.parse(data=data, strict=self._config.is_strict_mode)

    def build(self, data: m.FixtureListModel) -> m.RankingTableModel:
        """Invoke the factory build."""
        return self._factory.build(input=data)

    @staticmethod
    def sort(table: m.RankingTableModel) -> m.RankingTableModel:
        """Sort and return results."""
        table.sort()

        return table

    @property
    def stats(self) -> StatsCounter:
        """Return controller stats."""
        return self._stats
