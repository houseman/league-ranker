"""Unit test for the `ranker.factories` module."""

import pytest

from ranker import models as m
from ranker.factories import LogTableFactory


@pytest.fixture
def input():
    """A valid `FixtureListModel` instance."""
    return m.FixtureListModel(
        fixtures=[
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Lions"), score=m.ScoreModel(value=3)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Snakes"), score=m.ScoreModel(value=3)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Tarantulas"), score=m.ScoreModel(value=1)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Fc Awesome"), score=m.ScoreModel(value=0)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Lions"), score=m.ScoreModel(value=1)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Fc Awesome"), score=m.ScoreModel(value=1)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Tarantulas"), score=m.ScoreModel(value=3)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Snakes"), score=m.ScoreModel(value=5)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Lions"), score=m.ScoreModel(value=4)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Grouches"), score=m.ScoreModel(value=0)
                ),
            ),
        ]
    )


@pytest.fixture
def expected():
    """A valid `RankingTableModel` instance."""
    return m.RankingTableModel(
        rankings=[
            m.RankingModel(
                team=m.TeamModel(name="Lions"), points=m.RankPointsModel(value=5)
            ),
            m.RankingModel(
                team=m.TeamModel(name="Snakes"), points=m.RankPointsModel(value=4)
            ),
            m.RankingModel(
                team=m.TeamModel(name="Tarantulas"), points=m.RankPointsModel(value=3)
            ),
            m.RankingModel(
                team=m.TeamModel(name="Fc Awesome"), points=m.RankPointsModel(value=1)
            ),
            m.RankingModel(
                team=m.TeamModel(name="Grouches"), points=m.RankPointsModel(value=0)
            ),
        ]
    )


def test_build(input, expected):
    """
    Given:
    When:
    Then:
    """
    output = LogTableFactory.build(input)

    assert output == expected
