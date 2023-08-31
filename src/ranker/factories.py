"""Factories take in something and produce something else."""

import logging
from abc import ABC, abstractmethod

from . import models as m

logger = logging.getLogger(__name__)


class AbstractFactory(ABC):
    """An abstract class that describes the minimum required Factory functionality."""

    @abstractmethod
    def build(self, input: m.BaseModel) -> m.BaseModel:
        """A Factory must build something."""
        pass


class BaseFactory(AbstractFactory):
    """Base factory implementation."""

    def build(self, input: m.BaseModel) -> m.BaseModel:
        """Implement this method in all subclasses."""
        raise NotImplementedError()


class LogTableFactory(BaseFactory):
    """Factory produces a log table from match result data."""

    def build(self, input: m.InputMatchResultsModel) -> m.LogTableModel:  # type: ignore
        """Build a log table."""
        for result in input.results:
            left, right = result.left, result.right
            if left.score.points > right.score.points:
                logger.debug(
                    f"{left.team.name} won {right.team.name}: "
                    f"{left.score.points} - {right.score.points}"
                )
            elif right.score.points > left.score.points:
                logger.debug(
                    f"{right.team.name} won {left.team.name}: "
                    f"{right.score.points} - {left.score.points}"
                )
            else:
                logger.debug(
                    f"{left.team.name} drew {right.team.name}: "
                    f"{left.score.points} - {right.score.points}"
                )

        return m.LogTableModel(results=[])
