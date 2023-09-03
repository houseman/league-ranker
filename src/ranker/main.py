"""The application entry point."""


import logging
import os
from io import TextIOWrapper

import click
from tabulate import tabulate

from .configs import LeagueRankerConfig
from .controllers import LeagueRankController
from .requests import CreateLogTableRequest
from .utils import configure_logging, get_stats


@click.command()
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
    help="Sets the logger level",
    default=None,
    show_default=True,
)
def cli(
    input: TextIOWrapper,
    config_path: str | None,
    strict_parse: bool | None,
    verbose: bool | None,
    log_level: str | None,
) -> None:
    """
    Calculate and print the ranking table for a league.

    INPUT should be a input file path, or '-' for stdin.
    """
    # If set, let cli args override env, file values
    env = {}
    if config_path is not None:
        env["config_path"] = str(config_path)
    if strict_parse is not None:
        env["strict_parse"] = str(strict_parse)
    if verbose is not None:
        env["verbose"] = str(verbose)
    if log_level is not None:
        env["log_level"] = log_level

    config = LeagueRankerConfig.create(env)
    configure_logging()

    if config.get_bool("strict_parse", False):
        click.secho(
            f"{os.linesep}Note: Strict parsing is enabled.{os.linesep}",
            fg="red",
            bold=True,
        )
    if config.get_bool("verbose", False):
        click.secho(
            f"Using config: {config.get_str('config_path')}{os.linesep}",
            fg="blue",
        )

    request = CreateLogTableRequest(data=input.read())

    controller = LeagueRankController()
    response = controller.create_log_table(request=request)

    for i, ranking in enumerate(response.rankings, 1):
        name = ranking.team.name
        value = ranking.points.value
        print(f"{i}. {name}, {value} {'pt' if value == 1 else 'pts'}")

    if config.get_bool("verbose", False):
        stats = get_stats()

        headers = ["Imported", "Processed", "Failed"]
        rows = [[stats["read"], stats["parsed"], stats["error"]]]
        table = tabulate(rows, headers, tablefmt="fancy_grid")

        click.secho(f"{os.linesep*2}Statistics:", bold=True)
        click.echo(table)

    return None
