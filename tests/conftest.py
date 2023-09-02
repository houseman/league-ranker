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
    config.set("is_strict_parse", False)
    config.set("points_for_win", 3)
    config.set("points_for_loss", 0)
    config.set("points_for_draw", 1)
