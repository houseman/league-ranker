"""Module for useful utilities."""

import logging

from . import configs

_config = configs.LeagueRankerConfig()


def configure_logging(log_level: str) -> None:
    """Configure the Python logger."""
    level = logging.getLevelNamesMapping()[log_level]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.debug("Logging is configured")


def get_config() -> configs.LeagueRankerConfig:
    """Return a configuration instance."""
    return _config
