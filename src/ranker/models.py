"""Models are data containers."""
# ruff: noqa: D101 Missing docstring in public class

import typing as t
from dataclasses import dataclass


@dataclass
class TeamModel:
    name: str


@dataclass
class ScoreModel:
    points: int


@dataclass
class ResultModel:
    team: TeamModel
    score: ScoreModel


class MatchResultModel(t.NamedTuple):
    a: ResultModel
    b: ResultModel


InputDataSet: t.TypeAlias = list[MatchResultModel]
