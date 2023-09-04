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
class RankPointsModel:
    value: int


@dataclass
class RankingModel:
    team: TeamModel
    points: RankPointsModel


@dataclass
class RankingTableModel:
    rankings: list[RankingModel]
