"""Unit tests for the `ranker.parsers` module."""
import pytest

from ranker import models as m
from ranker.errors import RecordParseError
from ranker.models import FixtureListModel


def test_parse__valid_and_invalid():
    """
    Given: A valid input data
    When: Strict parsing is disabled
    Then: Return a valid FixtureListModel model.
    """
    from ranker.parsers import LeagueRankerParser

    data = (
        "Foo 1,Bar 2\nBaz 3, Bat Fox 4\r\nRed Jam 5 Sky Pen 6\n"
        "Fluff Mop 7,Kick Ball 8\r\n"
    )

    parser = LeagueRankerParser()
    parser._strict_parse = False

    expected = FixtureListModel(
        fixtures=[
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Foo"), score=m.ScoreModel(value=1)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Bar"), score=m.ScoreModel(value=2)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Baz"), score=m.ScoreModel(value=3)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Bat Fox"), score=m.ScoreModel(value=4)
                ),
            ),
            m.FixtureModel(
                left=m.ResultModel(
                    team=m.TeamModel(name="Fluff Mop"), score=m.ScoreModel(value=7)
                ),
                right=m.ResultModel(
                    team=m.TeamModel(name="Kick Ball"), score=m.ScoreModel(value=8)
                ),
            ),
        ]
    )

    output = parser.parse(data=data)

    assert output == expected
    assert parser._stats["read"] == 5
    assert parser._stats["error"] == 2
    assert parser._stats["parsed"] == 3


@pytest.mark.parametrize(
    ["record", "expected"],
    [
        ("Foo 3, Bar 5", ("Foo", "3", "Bar", "5")),
        ("Foo 3, Bar 5\n", ("Foo", "3", "Bar", "5")),
        ("Foo 3, Bar 5\r\n", ("Foo", "3", "Bar", "5")),
        ("Foo   Baz  13,   Baa Bar 0", ("Foo Baz", "13", "Baa Bar", "0")),
        ("$Foo 6, &Bar 5", ("Foo", "6", "Bar", "5")),
        ("Foo_Baz   13,   Baa   Bar 0", ("Foo Baz", "13", "Baa Bar", "0")),
        ("Foo_Baz_bar   1,   Baa _  Bar  _ 10", ("Foo Baz bar", "1", "Baa Bar", "10")),
        ("$_foo 6, _&Bar$foo 5", ("foo", "6", "Bar foo", "5")),
        ("Foo$Baz_Bar%3,(Bar)[20]", ("Foo Baz Bar", "3", "Bar", "20")),
    ],
)
def test_match__success__strict_mode_disabled(mocker, record, expected):
    """
    Given: A valid record string value, or one that can be normalised successfully
    When: Strict parsing is disabled
    Then: Return a valid tuple of four string values.
    """
    from ranker.parsers import LeagueRankerParser

    parser = LeagueRankerParser()
    parser._strict_parse = False

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
    from ranker.parsers import LeagueRankerParser

    parser = LeagueRankerParser()
    parser._strict_parse = True

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
    When: Strict parsing is disabled
    Then: Raise a RecordParseError.
    """
    from ranker.parsers import LeagueRankerParser

    parser = LeagueRankerParser()
    parser._strict_parse = False

    with pytest.raises(RecordParseError, match=match):
        parser.match(record=record)
