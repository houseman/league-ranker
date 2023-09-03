"""Meta classes."""

from typing import ParamSpec

P = ParamSpec("P")


class SingletonMeta(type):
    """Singleton meta class."""

    _instances: dict[type, type] = {}

    def __call__(cls, *args: P.args, **kwargs: P.kwargs) -> type:
        """Override the init."""
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]
