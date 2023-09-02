"""
Parsers understand a defined input data format.

They are able to convert input data to a model structure.
"""
from __future__ import annotations

import logging
import re
import typing as t

from . import errors as err
from . import models as m
from .utils import get_config

if t.TYPE_CHECKING:
    from .stats import StatsCounter

config = get_config()
logger = logging.getLogger(__name__)


class LeagueRankerParser:
    r"""
    A Parser for "League Ranker" format data.

    This data follows the record format

    ```
    ^(\D*) (\d+),(\D*) (\d+)$
    ```

    For example:
        "The Lions 3, Snakes 3"
    """

    _PATTERN: t.Final = r"^(\D*) (\d+),(\D*) (\d+)$"

    def __init__(self, stats: StatsCounter) -> None:
        """The constructor."""
        self._stats = stats
        self._is_strict_parse = config.get_bool("is_strict_parse", False)

    def parse(self, data: str) -> m.FixtureListModel:
        """Parse request input data."""
        results = []
        for record in re.split(r"\r\n|\n|\r", data):
            self._stats.incr("read")
            try:
                groups = self.match(record=record, strict=self._is_strict_parse)

            except err.RecordParseError as e:
                logger.warning(str(e))
                self._stats.incr("error")

                continue  # Skip to next record on error

            result = m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name=str(groups[0]).strip()),
                    score=m.ScoreModel(value=int(groups[1])),
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name=str(groups[2]).strip()),
                    score=m.ScoreModel(value=int(groups[3])),
                ),
            )
            logger.debug(f"Created model: {result}")
            self._stats.incr("parsed")
            results.append(result)

        return m.FixtureListModel(fixtures=results)

    @classmethod
    def match(cls, record: str, strict: bool = False) -> tuple[str, ...]:
        """
        Parse the given record string and return a tuple containing match group values.

        If parsing fails, a RecordParseError exception is raised.
        """
        if not strict:
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

        match = re.match(cls._PATTERN, record)

        if not match:
            raise err.RecordParseError(
                f"Invalid record format: '{record}' does not match {cls._PATTERN}"
            )

        groups = match.groups()

        return tuple([str(group).strip() for group in groups])  # Keep mypy happy ...
