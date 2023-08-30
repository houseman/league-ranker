"""Controller classes contain business and flow logic."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .parsers import BaseParser


class RankController:
    """Controller class contains logic for the League Ranker."""

    def __init__(self, parser: BaseParser) -> None:
        self._parser = parser

    def parse(self) -> None:
        """Invoke the parser."""
        model = self._parser.parse()
        print(model)

    def dump(self) -> None:
        """Dump the raw input data to output."""
        print(self._parser.reader.data)
