"""
Parsers understand a defined input data format.

They are able to convert input data to a model structure.
"""
from __future__ import annotations

import logging
import re
import typing as t
from abc import ABC, abstractmethod

from . import errors as err
from . import models as m

if t.TYPE_CHECKING:
    from .readers import BaseReader
    from .stats import StatsCounter

logger = logging.getLogger(__name__)


class AbstractParser(ABC):
    """Abstract Base Class defines minimum Reader functionality."""

    @abstractmethod
    def __init__(self, reader: BaseReader, stats: StatsCounter, strict: bool) -> None:
        """All Parsers will require a Reader."""
        pass

    @property
    @abstractmethod
    def reader(self) -> BaseReader:
        """Return the instance Reader object."""
        pass

    @abstractmethod
    def parse(self) -> m.InputMatchResultsModel:
        """All Parsers must parse reader data into a model."""
        pass


class BaseParser(AbstractParser):
    """Base Parser class."""

    def __init__(
        self, reader: BaseReader, stats: StatsCounter, strict: bool = False
    ) -> None:
        """The base constructor requires a Reader."""
        self._reader = reader
        self._strict = strict
        self._stats = stats

    @property
    def reader(self) -> BaseReader:
        """Return the instance Reader property."""
        return self._reader

    def parse(self) -> m.InputMatchResultsModel:
        """The parsing method must be implemented in subclasses."""
        raise NotImplementedError()


class LeagueRankerParser(BaseParser):
    r"""
    A reader for "League Ranker" format data.

    This data follows the record format

    ```
    ^(\D*) (\d+),(\D*) (\d+)$
    ```

    For example:
        "The Lions 3, Snakes 3"
    """

    _PATTERN: t.Final = r"^(\D*) (\d+),(\D*) (\d+)$"

    def parse(self) -> m.InputMatchResultsModel:
        """Parse reader input data."""
        results = []
        for record in re.split(r"\r\n|\n|\r", self.reader.data):
            self._stats.incr("read")
            try:
                groups = self.match(record=record)

            except err.RecordParseError as e:
                logger.warning(str(e))
                self._stats.incr("error")

                continue  # Skip to next record on error

            result = m.MatchResultModel(
                left=m.ResultModel(
                    team=m.TeamModel(name=str(groups[0]).strip()),
                    score=m.ScoreModel(points=int(groups[1])),
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name=str(groups[2]).strip()),
                    score=m.ScoreModel(points=int(groups[3])),
                ),
            )
            logger.debug(f"Created model: {result}")
            self._stats.incr("parsed")
            results.append(result)

        return m.InputMatchResultsModel(results=results)

    def match(self, record: str) -> tuple[str, ...]:
        """
        Parse the given record string and return a tuple containing match group values.

        If parsing fails, a RecordParseError exception is raised.
        """
        if not self._strict:
            """If strict mode is *not* enabled, try to normalise the data record.
            - Strip all characters that are not alphanumeric, space or comma
            - Replace underscores with spaces
            - Reduce consecutive spaces to a single space
            - Strip leading or ending spaces or newlines
            - Title-case words
            """
            record = re.sub(r"[^\w ,]+", " ", record)
            record = re.sub(r"[\s\_]+", " ", record)
            record = record.strip().title()

        if not record:
            raise err.RecordParseError(f"Unusable record: '{record}'")

        match = re.match(self._PATTERN, record)

        if not match:
            raise err.RecordParseError(
                f"Invalid record format: '{record}' does not match {self._PATTERN}"
            )

        groups = match.groups()

        return tuple([str(group).strip() for group in groups])  # Keep mypy happy ...
