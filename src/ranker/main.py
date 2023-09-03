"""The CLI application entry point."""

import logging
import os
import typing as t
from io import TextIOWrapper

import click
from tabulate import tabulate

from .config import LeagueRankerConfiguration
from .controllers import LeagueRankController
from .requests import CreateLogTableRequest
from .stats import LeagueRankerStats

P = t.ParamSpec("P")


@click.command()  # type: ignore
@click.argument("input", type=click.File(mode="r", encoding="locale"))
@click.option(
    "--config",
    "-c",
    "config_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path to a configuration file",
    default=None,
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
    help="Sets the logger level.",
    default=None,
    show_default=True,
)
def cli(*args: P.args, **kwargs: P.kwargs) -> None:
    """
    Calculate and print the ranking table for a league.

    INPUT should be a input file path, or '-' for stdin.
    """
    input = t.cast(TextIOWrapper, kwargs.pop("input"))  # This is the input file stream

    # If set, let cli args override env, file values
    config = LeagueRankerConfiguration.create(
        {k: v for k, v in kwargs.items() if v is not None}
    )

    click.echo()
    if config.get_bool("strict_parse", False):
        click.secho(
            f"Note: Strict parsing is enabled.{os.linesep}",
            fg="red",
            bold=True,
        )

    request = CreateLogTableRequest(data=input.read())

    controller = LeagueRankController()
    response = controller.create_log_table(request=request)

    for i, ranking in enumerate(response.rankings, 1):
        name = ranking.team.name
        value = ranking.points.value
        click.echo(f"{i}. {name}, {value} {'pt' if value == 1 else 'pts'}")

    if config.get_bool("verbose", False):
        stats = LeagueRankerStats()

        headers = ["Imported", "Processed", "Failed"]
        rows = [[stats["read"], stats["parsed"], stats["error"]]]
        table = tabulate(rows, headers, tablefmt="fancy_grid")

        click.secho(f"{os.linesep*2}Statistics:", bold=True)
        click.echo(table)

    return None
