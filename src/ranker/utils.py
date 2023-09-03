"""Module for miscellaneous utilities."""

import logging

from .configs import LeagueRankerConfig
from .stats import LeagueRankerStats


def configure_logging() -> None:
    """Configure the Python logger."""
    log_level = LeagueRankerConfig().get_str("log_level", "INFO")
    level = logging.getLevelNamesMapping()[log_level]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.debug(f"Logging is configured (level: {log_level})")


def get_stats() -> LeagueRankerStats:
    """Return a singleton stats instance."""
    return LeagueRankerStats()
