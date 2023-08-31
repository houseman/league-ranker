"""Request are an abstraction between the user interface and the controller."""
from dataclasses import dataclass


@dataclass
class CreateLogTableRequest:
    """Request for Log Table model."""

    data: str
