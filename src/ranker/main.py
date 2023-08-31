"""The application entry point."""

from __future__ import annotations

import logging
from io import TextIOWrapper

import click

from .configs import LeagueRankerConfig
from .controllers import LeagueRankController
from .factories import LogTableFactory
from .parsers import LeagueRankerParser
from .readers import BufferedTextStreamReader
from .stats import StatsCounter
from .utils import configure_logging


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
@click.option(
    "--log-level",
    type=click.Choice(
        [
            logging.getLevelName(logging.DEBUG),
            logging.getLevelName(logging.INFO),
            logging.getLevelName(logging.WARNING),
            logging.getLevelName(logging.ERROR),
            logging.getLevelName(logging.CRITICAL),
        ],
        case_sensitive=True,
    ),
    help="Sets the logger level",
    default=logging.getLevelName(logging.INFO),
    show_default=True,
)
def cli(input: TextIOWrapper | None, strict: bool, log_level: str) -> None:
    """Calculate and print the ranking table for a league."""
    configure_logging(log_level=log_level)

    if input:
        stream = input
    else:
        stream = TextIOWrapper(click.get_text_stream("stdin").buffer, encoding="locale")

    stats = StatsCounter()
    reader = BufferedTextStreamReader.load(stream=stream)
    config = LeagueRankerConfig(is_strict_mode=strict)
    parser = LeagueRankerParser(reader=reader, stats=stats, strict=strict)
    factory = LogTableFactory()

    controller = LeagueRankController(parser=parser, config=config, factory=factory)
    controller.dump()
    source = controller.parse()
    table = controller.build(source=source)
    for result in table.results:  # type: ignore
        print(f"{result.team.name}: {result.score.points}")  # type: ignore
    table.sort()  # type: ignore
    for result in table.results:  # type: ignore
        print(f"{result.team.name}: {result.score.points}")  # type: ignore

    click.secho("Stats", bold=True)
    click.secho("Records read: ", fg="green", nl=False)
    click.secho(stats["read"], fg="blue")
    click.secho("Records parsed: ", fg="green", nl=False)
    click.secho(stats["parsed"], fg="blue")
    click.secho("Records failed: ", fg="green", nl=False)
    click.secho(stats["error"], fg="blue")

    return None
