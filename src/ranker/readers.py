"""Readers take input data and store these."""

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    import io


class InputDataReader:
    """Buffered Text Stream reader."""

    @property
    def data(self) -> str:
        """Public accessor for class data."""
        return self._data

    def load_from_text(self, text: str) -> None:
        """Load data into Reader from a buffered text stream."""
        self._data = text

    def load_from_stream(self, stream: io.TextIOWrapper) -> None:
        """Load data into Reader from a buffered text stream."""
        self.load_from_text(stream.read())
