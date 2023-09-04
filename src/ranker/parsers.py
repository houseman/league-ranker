"""
Parsers understand a defined input data format.

They are able to convert input data to a model structure.
"""
import logging
import re
import typing as t

from . import errors as err
from . import models as m
from .config import LeagueRankerConfig
from .stats import LeagueRankerStats

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

    def __init__(self) -> None:
        """The constructor."""
        self._stats = LeagueRankerStats()
        self._strict_parse = LeagueRankerConfig().get_bool("strict_parse", False)

    def parse(self, data: str) -> m.FixtureListModel:
        """Parse request input data."""
        results = []
        for line, record in enumerate(re.split(r"\r\n|\n|\r", data)):
            self._stats.incr("read")
            try:
                groups = self.match(record=record, line=line + 1)

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

            self._stats.incr("parsed")
            results.append(result)

        return m.FixtureListModel(fixtures=results)

    def match(self, record: str, line: int = 0) -> tuple[str, ...]:
        """
        Parse the given record string and return a tuple containing match group values.

        If parsing fails, a RecordParseError exception is raised.
        """
        if not self._strict_parse:
            """If strict mode is *not* enabled, try to normalise the data record.
            - Strip all characters that are not alphanumeric, space or comma
            - Replace underscores with spaces
            - Reduce consecutive spaces to a single space
            - Strip leading and trailing spaces
            """
            record = re.sub(r"[^\w ,]+", " ", record)
            record = re.sub(r"[\s\_]+", " ", record)
            record = record.strip()

        if not record:
            raise err.RecordParseError(f"Unusable record: '{record}' at line {line}")

        match = re.match(self._PATTERN, record)

        if not match:
            raise err.RecordParseError(
                f"Invalid record format: '{record}' at line {line}"
            )

        groups = match.groups()

        return tuple([str(group).strip() for group in groups])  # Keep mypy happy ...
