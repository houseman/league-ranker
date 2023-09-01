"""Unit tests for the ranker.configs module."""


def test_config__is_singleton():
    """
    Given: That `LeagueRankerConfig` is a Singleton
    When: The class is created multiple times
    Then: All instances of that class should be the same instance
    """
    from ranker.configs import LeagueRankerConfig

    assert id(LeagueRankerConfig()) == id(LeagueRankerConfig())


def test_config__changes_persist():
    """
    Given:
    When:
    Then:
    """
    from ranker.configs import LeagueRankerConfig

    first = LeagueRankerConfig(is_strict_parse=False)
    second = LeagueRankerConfig(is_strict_parse=True)

    assert first == second
    assert first.is_strict_parse is False  # Not changed
    assert second.is_strict_parse is False  # Not changed
