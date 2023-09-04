"""Factories take in something and produce something else."""

import logging

from collections import defaultdict

from . import models as m
from .config import LeagueRankerConfig

logger = logging.getLogger(__name__)


# Constants for point values.
# These are only used if configuration values cannot be retrieved.
POINTS_WIN = 3
POINTS_LOSS = 0
POINTS_DRAW = 1


class LogTableFactory:
    """Factory produces a log table from match result data."""

    def __init__(self) -> None:
        self.points_win = LeagueRankerConfig().get_int("points_win") or POINTS_WIN
        self.points_loss = LeagueRankerConfig().get_int("points_loss") or POINTS_LOSS
        self.points_draw = LeagueRankerConfig().get_int("points_draw") or POINTS_DRAW

    def build(self, input: m.FixtureListModel) -> m.RankingTableModel:
        """Build a log table."""
        table: dict[str, int] = defaultdict(int)
        log_template = "{} {} {}: {} - {}"

        for fixture in input.fixtures:
            left, right = fixture.left, fixture.right

            format_args = [
                left.team.name,
                "",
                right.team.name,
                left.score.value,
                right.score.value,
            ]

            if left.score.value > right.score.value:
                format_args[1] = "won"
                table[left.team.name] += self.points_win
                table[right.team.name] += self.points_loss
            elif right.score.value > left.score.value:
                format_args[1] = "lost"
                table[left.team.name] += self.points_loss
                table[right.team.name] += self.points_win
            else:
                format_args[1] = "drew"
                table[left.team.name] += self.points_draw
                table[right.team.name] += self.points_draw

            logger.info(log_template.format(*format_args))

        rankings = [
            m.RankModel(
                team=m.TeamModel(name=k),
                aggregate=m.RankAggregateModel(value=v),
                order=m.RankOrderModel(value=0),  # Not yet sorted in rank order
            )
            for k, v in table.items()
        ]

        return m.RankingTableModel(rankings=rankings)
