"""Test cases for the stats counter."""
import pytest


def test_increment__valid_input__undefined_name():
    """
    Given: A state counter instance
    When: A valid integer is added to an undefined name
    Then: The named count is set to 1 or the given value.
    """
    from ranker.stats import StatsCounter

    stats = StatsCounter()

    stats.incr("foo")
    assert stats["foo"] == 1

    stats.incr("bat", 123)
    assert stats["bat"] == 123


def test_increment__valid_input__defined_name():
    """
    Given: A state counter instance
    When: A valid integer is added to defined name
    Then: The named count is incremented by the given value.
    """
    from ranker.stats import StatsCounter

    stats = StatsCounter()

    stats.incr("foo")
    assert stats["foo"] == 1

    stats.incr("foo", 100)
    assert stats["foo"] == 101


def test_increment__invalid_input():
    """
    Given: A state counter instance
    When: An invalid (non-integer) value is added
    Then: A ValueError is raised.
    """
    from ranker.stats import StatsCounter

    stats = StatsCounter()
    with pytest.raises(ValueError, match="Cannot add a non-integer: 'bar' given"):
        stats.incr("foo", "bar")


def test_increment__get_item():
    """
    Given: A state counter instance
    When: A non-defined name is accessed
    Then: A value of 0 is returned.
    """
    from ranker.stats import StatsCounter

    stats = StatsCounter()
    assert stats["red"] == 0
