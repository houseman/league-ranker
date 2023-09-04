"""Models are data containers."""
# ruff: noqa: D101 Missing docstring in public class

from dataclasses import dataclass


@dataclass
class TeamModel:
    name: str


@dataclass
class ScoreModel:
    value: int


@dataclass
class ResultModel:
    team: TeamModel
    score: ScoreModel


@dataclass
class FixtureModel:
    left: ResultModel
    right: ResultModel


@dataclass
class FixtureListModel:
    fixtures: list[FixtureModel]


@dataclass
class RankAggregateModel:
    """Points aggregated in ranking table."""

    value: int


@dataclass
class RankOrderModel:
    """
    Order in ranking table, based on aggregate points.

    This value will be equal for teams tha that have equivalent aggregate points.
    """

    value: int = 0


@dataclass
class RankModel:
    team: TeamModel
    aggregate: RankAggregateModel
    order: RankOrderModel


@dataclass
class RankingTableModel:
    rankings: list[RankModel]
