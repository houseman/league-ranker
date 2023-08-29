from __future__ import annotations

from abc import ABC, abstractmethod

import typing as t

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
    def load_from_stream(cls, stream: TextIOWrapper) -> AbstractReader:
        """Load Reader data from a text wrapper stream."""

        pass

    @classmethod
    @abstractmethod
    def load_from_text(cls, text: str) -> AbstractReader:
        """Load Reader data from a text object."""

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
    def load_from_stream(cls, stream: TextIOWrapper) -> BaseReader:
        data = stream.read()

        return cls(data=data)

    @classmethod
    def load_from_text(cls, text: str) -> BaseReader:
        return cls(data=text)


class LeagueRankerReader(BaseReader):
    """A reader for League Ranker format data
    This data follows the record format

    ```
    <NAME><space><SCORE><comma>[<space>]<NAME><space><SCORE><delimiter>
    ```

    For example:
        "Lions 3, Snakes 3\n"
    """

    pass
