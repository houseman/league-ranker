from __future__ import annotations

import click
import typing as t

from .controllers import RankController
from .readers import LeagueRankerReader

if t.TYPE_CHECKING:
    from io import TextIOWrapper


@click.command()
@click.option(
    "--input", type=click.File("r"), help="Path to data input file to read from"
)
def cli(input: TextIOWrapper | None) -> None:
    """Calculates the ranking table for a league"""
    if input:
        reader = LeagueRankerReader.load_from_stream(stream=input)
    else:
        reader = LeagueRankerReader.load_from_text(
            text=click.get_text_stream("stdin").read()
        )

    controller = RankController(reader=reader)
    controller.dump()

    return None
