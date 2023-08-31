"""Request are an abstraction between the user interface and the controller."""
from dataclasses import dataclass


@dataclass
class CreateLogTableRequest:
    """Request for Log Table model."""

    data: str

    def __post_init__(self) -> None:
        """Strip leading and ending spaces from data."""
        self.data = self.data.strip()
