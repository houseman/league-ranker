from dataclasses import dataclass

import typing as t


@dataclass
class TeamModel:
    name: str


@dataclass
class ScoreModel:
    team: TeamModel
    points: int


class ResultModel(t.NamedTuple):
    a: ScoreModel
    b: ScoreModel
