"""Readers take input data and store these."""

from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod

if t.TYPE_CHECKING:
    import io


class AbstractReader(ABC):
    """An abstract class defines the minimum required functionality for a Reader."""

    @property
    @abstractmethod
    def data(self) -> str:
        """Return the Reader's raw input data."""
        pass

    @classmethod
    @abstractmethod
    def load(cls, stream: t.Any) -> AbstractReader:
        """Load Reader data from a source."""
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
    def load(cls, stream: t.Any) -> BaseReader:
        """Implement in subclasses."""
        raise NotImplementedError()


class BufferedTextStreamReader(BaseReader):
    """Buffered Text Stream reader."""

    @classmethod
    def load(cls, stream: io.TextIOWrapper) -> BaseReader:
        """Load data into Reader from a buffered text stream."""
        data = stream.read()

        return cls(data=data.strip())
