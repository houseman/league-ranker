"""Models are data containers."""
# ruff: noqa: D101 Missing docstring in public class

from dataclasses import dataclass


@dataclass
class BaseModel:
    pass


@dataclass
class TeamModel(BaseModel):
    name: str


@dataclass
class ScoreModel(BaseModel):
    points: int


@dataclass
class ResultModel(BaseModel):
    team: TeamModel
    score: ScoreModel


@dataclass
class MatchResultModel(BaseModel):
    left: ResultModel
    right: ResultModel


@dataclass
class InputMatchResultsModel(BaseModel):
    results: list[MatchResultModel]


@dataclass
class LogTableModel(BaseModel):
    results: list[ResultModel]

    def sort(self) -> None:
        """Sort results by points descending, name ascending."""
        self.results.sort(key=lambda r: (r.score.points, r.team.name), reverse=True)
