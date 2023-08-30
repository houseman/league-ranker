"""A stats counter."""


class StatsCounter:
    """A simple stats counter."""

    def __init__(self) -> None:
        """Initialise teh counter."""
        self._stats: dict[str, int] = {}

    def incr(self, name: str, val: int = 1) -> None:
        """
        Increment a named count.

        If the name does not exist, it will be created.
        """
        if not isinstance(val, int):
            raise ValueError(f"Cannot add a non-integer: '{val}' given")

        self._stats[name] = self._stats.get(name, 0) + int(val)

    def __getitem__(self, name: str) -> int:
        """Retrieve a name's value using a dict-like interface."""
        return self._stats.get(name, 0)
