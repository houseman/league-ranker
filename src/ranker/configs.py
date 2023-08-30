"""Configuration classes."""
from dataclasses import dataclass


@dataclass
class BaseConfig:
    """Base configuration."""

    is_strict_mode: bool


@dataclass
class LeagueRankerConfig(BaseConfig):
    """Config implementation for League Ranker."""

    pass
