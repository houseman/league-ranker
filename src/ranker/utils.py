"""Module for useful utilities."""

import logging

from .configs import LeagueRankerConfig
from .stats import LeagueRankerStats


def configure_logging() -> None:
    """Configure the Python logger."""
    config = get_config()
    log_level = config.get_str("log_level", "INFO")
    level = logging.getLevelNamesMapping()[log_level]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.debug(f"Logging is configured (level: {log_level})")


def get_config() -> LeagueRankerConfig:
    """Return a singleton configuration instance."""
    return LeagueRankerConfig()


def get_stats() -> LeagueRankerStats:
    """Return a singleton stats instance."""
    return LeagueRankerStats()
