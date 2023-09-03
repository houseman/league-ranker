"""Factories take in something and produce something else."""

import logging

from . import models as m
from .config import LeagueRankerConfig

logger = logging.getLogger(__name__)


class LogTableFactory:
    """Factory produces a log table from match result data."""

    def __init__(self) -> None:
        self.points_win = LeagueRankerConfig().get_int("points_win") or 3
        self.points_loss = LeagueRankerConfig().get_int("points_loss") or 0
        self.points_draw = LeagueRankerConfig().get_int("points_draw") or 1

    def build(self, input: m.FixtureListModel) -> m.RankingTableModel:
        """Build a log table."""
        table: dict[str, int] = {}

        for fixture in input.fixtures:
            left, right = fixture.left, fixture.right

            left_points = 0
            right_points = 0

            if left.score.value > right.score.value:
                logger.debug(
                    f"{left.team.name} won {right.team.name}: "
                    f"{left.score.value} - {right.score.value}"
                )
                left_points = self.points_win
                right_points = self.points_loss
            elif right.score.value > left.score.value:
                logger.debug(
                    f"{right.team.name} won {left.team.name}: "
                    f"{right.score.value} - {left.score.value}"
                )
                left_points = self.points_loss
                right_points = self.points_win
            else:
                logger.debug(
                    f"{left.team.name} drew {right.team.name}: "
                    f"{left.score.value} - {right.score.value}"
                )
                # a draw (tie) is worth 1 point each
                left_points = self.points_draw
                right_points = self.points_draw

            # Add to table
            table[left.team.name] = table.get(left.team.name, 0) + left_points
            table[right.team.name] = table.get(right.team.name, 0) + right_points

        for k, v in table.items():
            logger.debug(f"{k}: {v}")

        return m.RankingTableModel(
            rankings=[
                m.RankingModel(
                    team=m.TeamModel(name=k), points=m.RankPointsModel(value=v)
                )
                for k, v in table.items()
            ]
        )
