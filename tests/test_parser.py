"""
Unit test for the Parser
"""
import pytest

from ranker.parsers import LeagueRankerParser
from ranker.readers import BufferedTextStreamReader
from ranker.errors import RecordParseError
from ranker import models as m


def test_parse__valid_and_invalid():
    data = (
        "Foo 1,Bar 2\nBaz 3, Bat Fox 4\r\nRed Jam 5 Sky Pen 6\n"
        "Fluff Mop 7,Kick Ball 8\r\n"
    )

    reader = BufferedTextStreamReader(data=data)
    parser = LeagueRankerParser(reader=reader)

    expected = [
        m.MatchResultModel(
            a=m.ResultModel(team=m.TeamModel(name="Foo"), score=m.ScoreModel(points=1)),
            b=m.ResultModel(team=m.TeamModel(name="Bar"), score=m.ScoreModel(points=2)),
        ),
        m.MatchResultModel(
            a=m.ResultModel(team=m.TeamModel(name="Baz"), score=m.ScoreModel(points=3)),
            b=m.ResultModel(
                team=m.TeamModel(name="Bat Fox"), score=m.ScoreModel(points=4)
            ),
        ),
        m.MatchResultModel(
            a=m.ResultModel(
                team=m.TeamModel(name="Fluff Mop"), score=m.ScoreModel(points=7)
            ),
            b=m.ResultModel(
                team=m.TeamModel(name="Kick Ball"), score=m.ScoreModel(points=8)
            ),
        ),
    ]

    output = parser.parse()

    assert output == expected


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
def test_match__success(record, expected):
    """
    Given: A record string value
    When: The record format is valid, or can be normalised successfully
    Then: Return a valid tuple of four string values
    """
    output = LeagueRankerParser.match(record=record)

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
def test_match__raises_record_parse_error(record, match):
    """
    Given: A record string value
    When: The record format is invalid, and can not be normalised successfully
    Then: Raise a RecordParseError
    """
    with pytest.raises(RecordParseError, match=match):
        LeagueRankerParser.match(record=record)
