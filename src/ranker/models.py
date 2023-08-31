"""Models are data containers."""
# ruff: noqa: D101 Missing docstring in public class

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


@dataclass
class MatchResultModel:
    left: ResultModel
    right: ResultModel


@dataclass
class InputMatchResultsModel:
    results: list[MatchResultModel]


@dataclass
class LogTableModel:
    results: list[ResultModel]

    def sort(self) -> None:
        """Sort results by points descending, name ascending."""
        self.results.sort(key=lambda r: (-r.score.points, r.team.name))
