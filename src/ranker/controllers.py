"""Controller classes contain business and flow logic."""

from __future__ import annotations

import typing as t

from .factories import LogTableFactory
from .parsers import LeagueRankerParser

if t.TYPE_CHECKING:
    from . import models as m
    from .requests import CreateLogTableRequest


class LeagueRankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(self) -> None:
        self._factory = LogTableFactory()
        self._parser = LeagueRankerParser()

    def create_log_table(self, request: CreateLogTableRequest) -> m.RankingTableModel:
        """Create and return a League Log Table."""
        parsed_data = self._parse(data=request.data)
        table = self._build(data=parsed_data)
        response = self._sort(table=table)

        return response

    def _parse(self, data: str) -> m.FixtureListModel:
        """Invoke the parser."""
        return self._parser.parse(data=data)

    def _build(self, data: m.FixtureListModel) -> m.RankingTableModel:
        """Invoke the factory build."""
        return self._factory.build(input=data)

    def _sort(self, table: m.RankingTableModel) -> m.RankingTableModel:
        """Sort rankings by points value descending, team name ascending."""
        table.rankings.sort(key=lambda r: (-r.points.value, r.team.name))

        return table
