from __future__ import annotations

import click

from .controllers import RankController
from .readers import LeagueRankerReader


from io import TextIOWrapper


@click.command()
@click.option(
    "--input",
    type=click.File(mode="r", encoding="locale"),
    help="Path to data input file to read from",
)
def cli(input: TextIOWrapper | None) -> None:
    """Calculates the ranking table for a league"""

    if input:
        stream = input
    else:
        stream = TextIOWrapper(click.get_text_stream("stdin").buffer, encoding="locale")

    reader = LeagueRankerReader.load(stream=stream)

    controller = RankController(reader=reader)
    controller.dump()

    return None
