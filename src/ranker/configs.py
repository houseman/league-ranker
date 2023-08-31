"""Configuration models for League Ranker."""
from dataclasses import dataclass


@dataclass
class LeagueRankerConfig:
    """Configuration model for League Ranker."""

    is_strict_mode: bool
