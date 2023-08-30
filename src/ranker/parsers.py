"""
Parsers understand a defined input data format.

They are able to convert input data to a model structure.
"""
from abc import ABC, abstractmethod

from . import models as m
from .readers import BaseReader


class AbstractParser(ABC):
    """Abstract Base Class defines minimum Reader functionality."""

    @abstractmethod
    def __init__(self, reader: BaseReader) -> None:
        """Abstract constructor requires a Reader."""
        pass

    @property
    @abstractmethod
    def reader(self) -> BaseReader:
        """Return the instance Reader object."""
        pass

    @abstractmethod
    def parse(self) -> m.InputDataSet:
        """Parse reader data into a model."""
        pass


class BaseParser(AbstractParser):
    """Base reader class."""

    def __init__(self, reader: BaseReader) -> None:
        """The base constructor requires a Reader."""
        self._reader = reader

    @property
    def reader(self) -> BaseReader:
        """Reader property."""
        return self._reader

    def parse(self) -> m.InputDataSet:
        """Implement in subclasses."""
        raise NotImplementedError()


class LeagueRankerParser(BaseParser):
    r"""
    A reader for "League Ranker" format data.

    This data follows the record format

    ```
    <NAME><space><SCORE><comma>[<space>]<NAME><space><SCORE><delimiter>
    ```

    For example:
        "Lions 3, Snakes 3\n"
    """

    def parse(self) -> m.InputDataSet:
        """Parse reader input data."""
        results = []
        for record in self.reader.data.split("\n"):
            if not record:
                continue

            left, right = record.split(",")
            result = m.MatchResultModel(
                a=self._parse_score(left.strip()), b=self._parse_score(right.strip())
            )
            print(result)
            results.append(result)

        return results

    def _parse_score(self, part: str) -> m.ResultModel:
        parts = part.split(" ")

        team = m.TeamModel(name=" ".join(parts[:-1]))
        return m.ResultModel(team=team, score=m.ScoreModel(points=int(parts[-1])))
