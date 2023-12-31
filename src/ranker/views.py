"""Views create a presentation layer."""

from __future__ import annotations

import os
import typing as t

import click

from tabulate import tabulate

from .config import LeagueRankerConfig
from .stats import LeagueRankerStats

if t.TYPE_CHECKING:
    from . import models as m


class CreateLogTableRequestView:
    """View deriver for the CreateLogTableRequest response."""

    @staticmethod
    def render(model: m.RankingTableModel) -> None:
        """Render to CLI."""
        for rank in model.rankings:
            order = rank.order.value
            name = rank.team.name
            aggregate = rank.aggregate.value
            click.echo(
                f"{order}. {name}, {aggregate} {'pt' if aggregate == 1 else 'pts'}"
            )

        if LeagueRankerConfig().get_bool("verbose", False):
            stats = LeagueRankerStats()

            headers = ["Imported", "Processed", "Failed"]
            rows = [[stats["read"], stats["parsed"], stats["error"]]]
            table = tabulate(rows, headers, tablefmt="fancy_grid")

            click.secho(f"{os.linesep*2}Statistics:", bold=True)
            click.echo(table)
