"""The application entry point."""

from __future__ import annotations

import logging
import os
from io import TextIOWrapper

import click
from tabulate import tabulate

from .controllers import LeagueRankController
from .requests import CreateLogTableRequest
from .utils import configure_logging, get_config

config = get_config()


@click.command()
@click.option(
    "--input",
    "-i",
    type=click.File(mode="r", encoding="locale"),
    help=(
        "Path to data input file to read from. "
        "If not specified, input will be read from stdin."
    ),
)
@click.option(
    "--strict",
    "-s",
    "strict_parse",
    is_flag=True,
    show_default=False,
    default=None,
    help="Enable strict parsing. Input values will not be normalised.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    show_default=False,
    default=None,
    help="Run verbosely (prints statistics at completion).",
)
@click.option(
    "--log-level",
    "-l",
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
    default=None,  # logging.getLevelName(logging.INFO),
    show_default=True,
)
def cli(
    input: TextIOWrapper | None,
    strict_parse: bool | None,
    verbose: bool | None,
    log_level: str | None,
) -> None:
    """Calculate and print the ranking table for a league."""
    print(f"CONFIG: {config._data}")
    # Let cli argus override env, file values by setting mutate=True
    if strict_parse is not None:
        config.set("strict_parse", strict_parse, mutate=True)
    if verbose is not None:
        config.set("verbose", verbose, mutate=True)
    if log_level is not None:
        config.set("log_level", log_level, mutate=True)

    configure_logging()

    if config.get_bool("strict_parse", False):
        click.secho(
            f"{os.linesep}Note: Strict parsing is enabled.{os.linesep}",
            fg="red",
            bold=True,
        )

    if input:
        # From --input cli parameter
        data = input.read()
    else:
        # From STDIN
        data = TextIOWrapper(
            click.get_text_stream("stdin").buffer, encoding="locale"
        ).read()

    request = CreateLogTableRequest(data=data)

    controller = LeagueRankController()
    response = controller.create_log_table(request=request)

    for i, ranking in enumerate(response.rankings, 1):
        name = ranking.team.name
        value = ranking.points.value
        print(f"{i}. {name}, {value} {'pt' if value == 1 else 'pts'}")

    if config.get_bool("verbose", False):
        stats = controller.stats

        headers = ["Imported", "Processed", "Failed"]
        rows = [[stats["read"], stats["parsed"], stats["error"]]]
        table = tabulate(rows, headers, tablefmt="fancy_grid")

        click.secho(f"{os.linesep*2}Statistics:", bold=True)
        click.echo(table)

    return None
