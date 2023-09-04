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
                    team=m.TeamModel(name="FC Awesome"), score=m.ScoreModel(value=0)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Lions"), score=m.ScoreModel(value=1)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="FC Awesome"), score=m.ScoreModel(value=1)
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
            m.RankModel(
                team=m.TeamModel(name="Lions"),
                aggregate=m.RankAggregateModel(value=5),
                order=m.RankOrderModel(value=0),
            ),
            m.RankModel(
                team=m.TeamModel(name="Snakes"),
                aggregate=m.RankAggregateModel(value=4),
                order=m.RankOrderModel(value=0),
            ),
            m.RankModel(
                team=m.TeamModel(name="Tarantulas"),
                aggregate=m.RankAggregateModel(value=3),
                order=m.RankOrderModel(value=0),
            ),
            m.RankModel(
                team=m.TeamModel(name="FC Awesome"),
                aggregate=m.RankAggregateModel(value=1),
                order=m.RankOrderModel(value=0),
            ),
            m.RankModel(
                team=m.TeamModel(name="Grouches"),
                aggregate=m.RankAggregateModel(value=0),
                order=m.RankOrderModel(value=0),
            ),
        ]
    )


def test_build(input, expected):
    """
    Given:
    When:
    Then:
    """
    factory = LogTableFactory()
    output = factory.build(input)

    assert output == expected
