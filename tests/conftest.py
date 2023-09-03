"""Pytest fixtures for this module"""

import pytest


@pytest.fixture(autouse=True)
def singleton(mocker):
    """Patch the SingletonMeta class to disable Singleton behaviour."""
    from ranker.meta import SingletonMeta

    def patch_call(cls, *args, **kwargs):
        return type.__call__(cls, *args, **kwargs)

    mocker.patch.object(SingletonMeta, "__call__", patch_call)


@pytest.fixture(autouse=True)
def config():
    """Use this configuration in test cases."""
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config.set("strict_parse", False)
    config.set("points_win", 3)
    config.set("points_loss", 0)
    config.set("points_draw", 1)


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
  log_level: INFO
  strict_parse: false
  verbose: false
  points_win: 3 # A win is worth 3 points
  points_loss: 0 # A loss is worth 0 points
  points_draw: 1 # A draw is worth 1 point
"""
