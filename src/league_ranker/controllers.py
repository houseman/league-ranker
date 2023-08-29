from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .readers import BaseReader


class RankController:
    """Controller class contains logic for the League Ranker"""

    def __init__(self, reader: BaseReader) -> None:
        self._reader = reader
        self._reader.parse()

    def dump(self) -> None:
        """Dump the raw input data to output."""

        print(self._reader.data)
