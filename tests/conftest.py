"""Pytest fixtures for all modules."""

import pytest

from ranker import models as m


@pytest.fixture(autouse=True)
def singleton(mocker):
    """Patch the SingletonMeta class to *disable* Singleton behaviour."""
    from ranker.meta import SingletonMeta

    def patch_call(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)

    mocker.patch.object(SingletonMeta, "__call__", patch_call)


@pytest.fixture(autouse=True)
def config(mocker, config_yaml):
    """Use this configuration in test cases."""
    import yaml

    from ranker.config import LeagueRankerConfig

    mocker.patch.object(LeagueRankerConfig, "_merge_from_file")

    LeagueRankerConfig.create(yaml.safe_load(config_yaml).get("config", {}))


@pytest.fixture
def valid_input_data():
    """Valid input data fixture."""
    return """Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
Lions 1, FC Awesome 1
Tarantulas 3, Snakes 1
Lions 4, Grouches 0"""


@pytest.fixture
def invalid_input_data():
    """Valid input data fixture."""
    return """Lions 3 Snakes 3
Tarantulas 1 FC Awesome 0
Lions 1 FC Awesome 1
Tarantulas 3 Snakes 1
Lions 4 Grouches 0"""


@pytest.fixture
def config_yaml():
    """Valid configuration YAML."""
    return """config:
  log_level: ERROR
  config_path: /var/foo/bar.yaml
  strict_parse: false
  verbose: false
  points_win: 3 # A win is worth 3 aggregate points
  points_loss: 0 # A loss is worth 0 aggregate points
  points_draw: 1 # A draw is worth 1 aggregate point
"""


@pytest.fixture
def sorted_log_table():
    """A sorted `RankingTableModel` instance."""
    return m.RankingTableModel(
        rankings=[
            m.RankModel(
                team=m.TeamModel(name="Tarantulas"),
                aggregate=m.RankAggregateModel(value=6),
                order=m.RankOrderModel(value=1),
            ),
            m.RankModel(
                team=m.TeamModel(name="Lions"),
                aggregate=m.RankAggregateModel(value=5),
                order=m.RankOrderModel(value=2),
            ),
            m.RankModel(
                team=m.TeamModel(name="FC Awesome"),
                aggregate=m.RankAggregateModel(value=1),
                order=m.RankOrderModel(value=3),
            ),
            m.RankModel(
                team=m.TeamModel(name="Snakes"),
                aggregate=m.RankAggregateModel(value=1),
                order=m.RankOrderModel(value=3),
            ),
            m.RankModel(
                team=m.TeamModel(name="Grouches"),
                aggregate=m.RankAggregateModel(value=0),
                order=m.RankOrderModel(value=5),
            ),
        ]
    )
