"""Readers take input data and store these."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    import io


class BufferedTextStreamReader:
    """Buffered Text Stream reader."""

    def __init__(self, data: str) -> None:
        self._data = data

    @property
    def data(self) -> str:
        """Public accessor for class data."""
        return self._data

    @classmethod
    def load(cls, stream: io.TextIOWrapper) -> BufferedTextStreamReader:
        """Load data into Reader from a buffered text stream."""
        data = stream.read()

        return cls(data=data.strip())
