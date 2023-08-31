"""The application entry point."""

from __future__ import annotations

import logging
from io import TextIOWrapper

import click

from .configs import LeagueRankerConfig
from .controllers import LeagueRankController
from .requests import CreateLogTableRequest
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
    "--verbose",
    is_flag=True,
    show_default=True,
    default=False,
    help="Run verbosely; prints statistics at completion",
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
def cli(
    input: TextIOWrapper | None, strict: bool, verbose: bool, log_level: str
) -> None:
    """Calculate and print the ranking table for a league."""
    configure_logging(log_level=log_level)

    if input:
        # From --input cli parameter
        data = input.read()
    else:
        # From STDIN
        data = TextIOWrapper(
            click.get_text_stream("stdin").buffer, encoding="locale"
        ).read()

    request = CreateLogTableRequest(data=data)
    config = LeagueRankerConfig(is_strict_mode=strict)

    controller = LeagueRankController(config=config)
    response = controller.create_log_table(request=request)

    for ranking in response.rankings:
        print(f"{ranking.team.name}: {ranking.value.value}")

    if verbose:
        stats = controller.stats

        click.secho("Stats", bold=True)
        click.secho("Records read: ", fg="green", nl=False)
        click.secho(stats["read"], fg="blue")
        click.secho("Records parsed: ", fg="green", nl=False)
        click.secho(stats["parsed"], fg="blue")
        click.secho("Records failed: ", fg="green", nl=False)
        click.secho(stats["error"], fg="blue")

    return None
