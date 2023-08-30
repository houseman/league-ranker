"""Readers take input data and store these."""

from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

from . import models as m

if t.TYPE_CHECKING:
    from io import TextIOWrapper


class AbstractReader(ABC):
    """An abstract class defines the minimum required functionality for a Reader."""

    @property
    @abstractmethod
    def data(self) -> str:
        """Return the Reader's raw input data."""
        pass

    @classmethod
    @abstractmethod
    def load(cls, stream: TextIOWrapper) -> AbstractReader:
        """Load Reader data from a buffered text stream."""
        pass

    @abstractmethod
    def parse(self) -> None:
        """Parse loaded reader data into a data model."""
        pass


class BaseReader(AbstractReader):
    """
    A base class for data readers.

    If you need to create a reader for a new data format, extend this class.
    """

    def __init__(self, data: str) -> None:
        self._data = data

    @property
    def data(self) -> str:
        """Public accessor for class data."""
        return self._data

    @classmethod
    def load(cls, stream: TextIOWrapper) -> BaseReader:
        """Load data into Reader from a buffered text stream."""
        data = stream.read()

        return cls(data=data)

    def parse(self) -> None:
        """Parse input data."""
        return None  # pragma: no cover


class LeagueRankerReader(BaseReader):
    r"""
    A reader for "League Ranker" format data.

    This data follows the record format

    ```
    <NAME><space><SCORE><comma>[<space>]<NAME><space><SCORE><delimiter>
    ```

    For example:
        "Lions 3, Snakes 3\n"
    """

    def parse(self) -> None:
        """Parse input data."""
        for record in self._data.split("\n"):
            if not record:
                continue

            left, right = record.split(",")
            result = m.MatchResultModel(
                a=self._parse_score(left.strip()), b=self._parse_score(right.strip())
            )
            print(result)

        return None

    def _parse_score(self, part: str) -> m.ResultModel:
        parts = part.split(" ")

        team = m.TeamModel(name=" ".join(parts[:-1]))
        return m.ResultModel(team=team, score=m.ScoreModel(points=int(parts[-1])))
