"""Module for useful utilities."""

import logging


def configure_logging(log_level: str) -> None:
    """Configure the Python logger."""
    level = logging.getLevelNamesMapping()[log_level]
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
