"""Controller classes contain business and flow logic."""

from __future__ import annotations

import logging
import typing as t

from .factories import LogTableFactory
from .parsers import LeagueRankerParser

if t.TYPE_CHECKING:
    from . import models as m
    from .requests import CreateLogTableRequest

logger = logging.getLogger()


class LeagueRankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(self) -> None:
        self._factory = LogTableFactory()
        self._parser = LeagueRankerParser()

    def create_log_table(self, request: CreateLogTableRequest) -> m.RankingTableModel:
        """Create and return a League Log Table."""
        parsed_data = self._parse(data=request.data)
        table = self._build(data=parsed_data)
        response = self._rank(table=table)

        return response

    def _parse(self, data: str) -> m.FixtureListModel:
        """Invoke the parser."""
        return self._parser.parse(data=data)

    def _build(self, data: m.FixtureListModel) -> m.RankingTableModel:
        """Invoke the factory build."""
        return self._factory.build(input=data)

    def _rank(self, table: m.RankingTableModel) -> m.RankingTableModel:
        """Assign rank order amd sort table by this order."""
        # First, sort the table by aggregate value descending
        table.rankings.sort(key=lambda r: (-r.aggregate.value, r.team.name))

        current_aggregate = None
        current_order = 0

        for current_sequence, rank in enumerate(table.rankings, start=1):
            if rank.aggregate.value != current_aggregate:
                current_aggregate = rank.aggregate.value
                current_order += current_sequence - current_order

            logger.debug(f"Set {rank.team.name} to order {current_order}")
            rank.order.value = current_order

        return table
