"""Unit test for the Parser."""
import secrets

import pytest

from ranker import models as m
from ranker.errors import RecordParseError
from ranker.models import InputMatchResultsModel
from ranker.parsers import LeagueRankerParser
from ranker.requests import GetLogTableRequest
from ranker.stats import StatsCounter


def test_parse__valid_and_invalid():
    """
    Given: A valid input data
    When: Strict parsing is disabled
    Then: Return a valid InputMatchResultsModel model.
    """
    data = (
        "Foo 1,Bar 2\nBaz 3, Bat Fox 4\r\nRed Jam 5 Sky Pen 6\n"
        "Fluff Mop 7,Kick Ball 8\r\n"
    )

    stats = StatsCounter()
    request = GetLogTableRequest()
    request.load_from_text(text=data)
    parser = LeagueRankerParser(request=request, stats=stats, strict=False)

    expected = InputMatchResultsModel(
        results=[
            m.MatchResultModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Foo"), score=m.ScoreModel(points=1)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Bar"), score=m.ScoreModel(points=2)
                ),
            ),
            m.MatchResultModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Baz"), score=m.ScoreModel(points=3)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Bat Fox"), score=m.ScoreModel(points=4)
                ),
            ),
            m.MatchResultModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Fluff Mop"), score=m.ScoreModel(points=7)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Kick Ball"), score=m.ScoreModel(points=8)
                ),
            ),
        ]
    )

    output = parser.parse()

    assert output == expected
    assert stats["read"] == 5
    assert stats["error"] == 2
    assert stats["parsed"] == 3


@pytest.mark.parametrize(
    ["record", "expected"],
    [
        ("Foo 3, Bar 5", ("Foo", "3", "Bar", "5")),
        ("Foo 3, Bar 5\n", ("Foo", "3", "Bar", "5")),
        ("Foo 3, Bar 5\r\n", ("Foo", "3", "Bar", "5")),
        ("Foo   Baz  13,   Baa Bar 0", ("Foo Baz", "13", "Baa Bar", "0")),
        ("$Foo 6, &Bar 5", ("Foo", "6", "Bar", "5")),
        ("Foo_Baz   13,   Baa   Bar 0", ("Foo Baz", "13", "Baa Bar", "0")),
        ("Foo_Baz_bar   1,   Baa _  Bar  _ 10", ("Foo Baz Bar", "1", "Baa Bar", "10")),
        ("$_foo 6, _&Bar$foo 5", ("Foo", "6", "Bar Foo", "5")),
        ("Foo$Baz_Bar%3,(Bar)[20]", ("Foo Baz Bar", "3", "Bar", "20")),
    ],
)
def test_match__success__strict_mode_disabled(mocker, record, expected):
    """
    Given: A valid record string value, or one that can be normalised successfully
    When: Strict parsing is disabled
    Then: Return a valid tuple of four string values.
    """
    parser = LeagueRankerParser(
        request=mocker.Mock(), stats=mocker.Mock(), strict=False
    )

    output = parser.match(record=record)

    assert output == expected


@pytest.mark.parametrize(
    ["record", "expected"],
    [
        ("Foo 3, Bar 5", ("Foo", "3", "Bar", "5")),
        ("Foo Red 7, Bar Baz 15", ("Foo Red", "7", "Bar Baz", "15")),
    ],
)
def test_match__success__strict_mode_enabled(mocker, record, expected):
    """
    Given: A valid record string value
    When: Strict parsing is enabled
    Then: Return a valid tuple of four string values.
    """
    parser = LeagueRankerParser(request=mocker.Mock(), stats=mocker.Mock(), strict=True)

    output = parser.match(record=record)

    assert output == expected


@pytest.mark.parametrize(
    ["record", "match"],
    [
        ("", r"Unusable record:"),
        ("Foo 3 Bar 5", r"Invalid record format:"),
        ("The quick, brown fox", r"Invalid record format:"),
        ("Foo3Bar5", r"Invalid record format:"),
        ("Foo3,Bar5", r"Invalid record format:"),
        ("Foo 1, Bar 1, Foo 1, Bar 1", r"Invalid record format:"),
    ],
)
def test_match__raises_record_parse_error(mocker, record, match):
    """
    Given: Am invalid data record
    When: Strict parsing is either enabled or disabled
    Then: Raise a RecordParseError.
    """
    strict = secrets.choice([True, False])
    parser = LeagueRankerParser(
        request=mocker.Mock(), stats=mocker.Mock(), strict=strict
    )

    with pytest.raises(RecordParseError, match=match):
        parser.match(record=record)
