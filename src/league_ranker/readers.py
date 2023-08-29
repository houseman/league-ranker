from __future__ import annotations

from abc import ABC, abstractmethod
import typing as t

from . import models as m

if t.TYPE_CHECKING:
    from io import TextIOWrapper


class AbstractReader(ABC):
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
        """Parse loaded reader data into a data model"""

        pass


class BaseReader(AbstractReader):
    """A base class for data readers.

    If you need to create a reader for a new data format, extend this class.
    """

    def __init__(self, data: str) -> None:
        self._data = data

    @property
    def data(self) -> str:
        return self._data

    @classmethod
    def load(cls, stream: TextIOWrapper) -> BaseReader:
        data = stream.read()

        return cls(data=data)

    def parse(self) -> None:
        return None  # pragma: no cover


class LeagueRankerReader(BaseReader):
    """A reader for "League Ranker" format data
    This data follows the record format
    ```
    <NAME><space><SCORE><comma>[<space>]<NAME><space><SCORE><delimiter>
    ```

    For example:
        "Lions 3, Snakes 3\n"
    """

    def parse(self) -> None:
        for record in self._data.split("\n"):
            if not record:
                continue

            left, right = record.split(",")
            result = m.ResultModel(
                a=self._parse_score(left.strip()), b=self._parse_score(right.strip())
            )
            print(result)

        return None

    def _parse_score(self, part: str) -> m.ScoreModel:
        parts = part.split(" ")

        team = m.TeamModel(name=" ".join(parts[:-1]))
        return m.ScoreModel(team=team, points=int(parts[-1]))
