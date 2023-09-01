"""Configuration models for League Ranker."""

from dataclasses import dataclass

from ranker.meta import SingletonMeta


@dataclass(frozen=True)
class LeagueRankerConfig(metaclass=SingletonMeta):
    """Configuration model for League Ranker."""

    is_strict_parse: bool = False
    points_for_win: int = 3  # A win is worth 3 points
    points_for_loss: int = 0  # A loss is worth 0 points
    points_for_draw: int = 1  # A draw is worth 1 point
