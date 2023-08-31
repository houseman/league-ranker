"""Factories take in something and produce something else."""

import logging

from . import models as m

logger = logging.getLogger(__name__)


class LogTableFactory:
    """Factory produces a log table from match result data."""

    @staticmethod
    def build(input: m.FixtureListModel) -> m.RankingTableModel:
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
                left_points = 3  # A win is worth 3 points
            elif right.score.value > left.score.value:
                logger.debug(
                    f"{right.team.name} won {left.team.name}: "
                    f"{right.score.value} - {left.score.value}"
                )
                right_points = 3  # A win is worth 3 points
            else:
                logger.debug(
                    f"{left.team.name} drew {right.team.name}: "
                    f"{left.score.value} - {right.score.value}"
                )
                # a draw (tie) is worth 1 point each
                left_points = 1
                right_points = 1

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
