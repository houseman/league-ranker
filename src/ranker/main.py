"""The application entry point."""

from __future__ import annotations

from io import TextIOWrapper

import click

from .configs import LeagueRankerConfig
from .controllers import RankController
from .parsers import LeagueRankerParser
from .readers import BufferedTextStreamReader


@click.command()
@click.option(
    "--input",
    type=click.File(mode="r", encoding="locale"),
    help="Path to data input file to read from",
)
@click.option(
    "--strict",
    is_flag=True,
    show_default=True,
    default=False,
    help="Run in strict mode. Input values will not be normalised",
)
def cli(input: TextIOWrapper | None, strict: bool) -> None:
    """Calculate and print the ranking table for a league."""
    if input:
        stream = input
    else:
        stream = TextIOWrapper(click.get_text_stream("stdin").buffer, encoding="locale")

    reader = BufferedTextStreamReader.load(stream=stream)
    config = LeagueRankerConfig(is_strict_mode=strict)
    parser = LeagueRankerParser(reader=reader, strict=strict)

    controller = RankController(parser=parser, config=config)
    controller.dump()
    controller.parse()

    return None
