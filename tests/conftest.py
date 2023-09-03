"""Pytest fixtures for all modules."""

import pytest


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

    from ranker.configurations import LeagueRankerConfiguration

    mocker.patch.object(LeagueRankerConfiguration, "_load_from_file")

    LeagueRankerConfiguration.create(yaml.safe_load(config_yaml).get("config", {}))


@pytest.fixture
def valid_input_data():
    """Valid input data fixture."""
    return """Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
Lions 1, FC Awesome 1
Tarantulas 3, Snakes 1
Lions 4, Grouches 0"""


@pytest.fixture
def config_yaml():
    """Valid configuration YAML."""
    return """config:
  log_level: ERROR
  config_path: /var/foo/bar.yaml
  strict_parse: false
  verbose: false
  points_win: 3 # A win is worth 3 points
  points_loss: 0 # A loss is worth 0 points
  points_draw: 1 # A draw is worth 1 point
"""
