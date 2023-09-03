"""Unit tests for the `ranker.controllers` module."""
from ranker import models as m
from ranker.requests import CreateLogTableRequest


def test_create_log_table__valid_input_data(valid_input_data, sorted_log_table):
    """
    Given: A `CreateLogTableRequest`
    When: The request data is valid
    Then: Return a sorted log table
    """
    from ranker.controllers import LeagueRankController

    controller = LeagueRankController()

    request = CreateLogTableRequest(data=valid_input_data)

    output = controller.create_log_table(request=request)

    assert output == sorted_log_table


def test_create_log_table__invalid_input_data(invalid_input_data):
    """
    Given: A `CreateLogTableRequest`
    When: The request data is invalid
    Then: Return an empty results
    """
    from ranker.controllers import LeagueRankController

    controller = LeagueRankController()

    request = CreateLogTableRequest(data=invalid_input_data)

    output = controller.create_log_table(request=request)

    assert output == m.RankingTableModel(rankings=[])
