"""Module for useful utilities."""

import logging

from . import configs


def configure_logging(log_level: str) -> None:
    """Configure the Python logger."""
    level = logging.getLevelNamesMapping()[log_level]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.debug(f"Logging is configured (level: {log_level})")


def get_config() -> configs.LeagueRankerConfig:
    """Return a singleton configuration instance."""
    return configs.LeagueRankerConfig()
