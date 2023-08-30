"""
Parsers understand a defined input data format.

They are able to convert input data to a model structure.
"""
import logging
import re
import typing as t
from abc import ABC, abstractmethod

from . import errors as err
from . import models as m
from .readers import BaseReader

logger = logging.getLogger(__name__)


class AbstractParser(ABC):
    """Abstract Base Class defines minimum Reader functionality."""

    @abstractmethod
    def __init__(self, reader: BaseReader) -> None:
        """All Parsers will require a Reader."""
        pass

    @property
    @abstractmethod
    def reader(self) -> BaseReader:
        """Return the instance Reader object."""
        pass

    @abstractmethod
    def parse(self) -> m.InputDataSet:
        """All Parsers must parse reader data into a model."""
        pass


class BaseParser(AbstractParser):
    """Base Parser class."""

    def __init__(self, reader: BaseReader) -> None:
        """The base constructor requires a Reader."""
        self._reader = reader

    @property
    def reader(self) -> BaseReader:
        """Return the instance Reader property."""
        return self._reader

    def parse(self) -> m.InputDataSet:
        """The parsing method must be implemented in subclasses."""
        raise NotImplementedError()  # pragma: no cover


class LeagueRankerParser(BaseParser):
    r"""
    A reader for "League Ranker" format data.

    This data follows the record format

    ```
    ^([^\d)]*) (\d+),([^\d)]*) (\d+)$
    ```

    For example:
        "Lions 3, Snakes 3"
    """

    _PATTERN: t.Final = r"^([^\d)]*) (\d+),([^\d)]*) (\d+)$"

    def parse(self) -> m.InputDataSet:
        """Parse reader input data."""
        results = []
        for record in re.split(r"\r\n|\n|\r", self.reader.data):
            try:
                groups = self.match(record=record)

            except err.RecordParseError as e:
                logger.warning(str(e))

                continue  # Skip to next record on error

            result = m.MatchResultModel(
                a=m.ResultModel(
                    team=m.TeamModel(name=str(groups[0]).strip()),
                    score=m.ScoreModel(points=int(groups[1])),
                ),
                b=m.ResultModel(
                    team=m.TeamModel(name=str(groups[2]).strip()),
                    score=m.ScoreModel(points=int(groups[3])),
                ),
            )
            logger.debug(f"Created model: {result}")
            results.append(result)

        return results

    @classmethod
    def match(cls, record: str) -> tuple[str, ...]:
        """
        Parse the given record string and return a tuple containing match group values.

        If parsing fails, a RecordParseError exception is raised.
        """
        record = re.sub(r"[^\w ,]+", " ", record)
        record = re.sub(r"[\s\_]+", " ", record)
        record = record.strip().title()

        if not record:
            raise err.RecordParseError(f"Unusable record: '{record}'")

        match = re.match(cls._PATTERN, record)

        if not match:
            raise err.RecordParseError(
                f"Invalid record format: '{record}' does not match {cls._PATTERN}"
            )

        groups = match.groups()

        return tuple([str(group).strip() for group in groups])  # Keep mypy happy ...
