"""The application entry point."""

from __future__ import annotations

from io import TextIOWrapper

import click

from .controllers import RankController
from .readers import LeagueRankerReader


@click.command()
@click.option(
    "--input",
    type=click.File(mode="r", encoding="locale"),
    help="Path to data input file to read from",
)
def cli(input: TextIOWrapper | None) -> None:
    """Calculate and print the ranking table for a league."""
    if input:
        stream = input
    else:
        stream = TextIOWrapper(click.get_text_stream("stdin").buffer, encoding="locale")

    reader = LeagueRankerReader.load(stream=stream)

    controller = RankController(reader=reader)
    controller.dump()

    return None
