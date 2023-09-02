"""Unit tests for the ranker.configs module."""
import os

import pytest

from ranker.errors import ConfigurationError


@pytest.fixture
def config():
    """
    Disable the `config` auto fixture for these tests.

    See `tests/conftest.py`
    """
    pass


def test_config__args_or_kwargs_in_constructor_raises_config_error():
    """
    Given: Create a new `LeagueRankerConfig` instance
    When: Passing args or keyword args to the constructor
    Then: Raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    with pytest.raises(ConfigurationError):
        LeagueRankerConfig(12)

    with pytest.raises(ConfigurationError):
        LeagueRankerConfig(foo="bar")


@pytest.mark.parametrize(
    "value, expected",
    [(111213, "111213"), ("The", "The"), ("04567", "04567"), (True, "True")],
)
def test_get_str__key_value_is_set(value, expected):
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a string value for a key that is set
    Then: Return the string value for that key
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._merge({"foo": value})

    assert config.get_str("foo") == expected


def test_get_str__key_value_is_not_set_no_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a string value for a key that is not set, with no default value
    Then: raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    with pytest.raises(ConfigurationError, match="Configuration key 'foo' is not set"):
        config.get_str("foo")


def test_get_str__key_value_is_not_set_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a string value for a key that is not set, and a default value
    Then: Return the default value
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    assert config.get_str("foo", "baz") == "baz"


@pytest.mark.parametrize(
    "value, expected",
    [("0", 0), ("12345", 12345), ("04567", 4567), (111213, 111213), (0, 0)],
)
def test_get_int__key_value_is_set(value, expected):
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting an integer value for a key that is set
    Then: Return the integer value for that key
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._merge({"bar": value})

    assert config.get_int("bar") == expected


def test_get_int__key_value_is_not_set_no_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting an integer value for a key that is set, with no default value
    Then: raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    with pytest.raises(ConfigurationError, match="Configuration key 'foo' is not set"):
        config.get_int("foo")


def test_get_int__key_value_is_not_set_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting an integer value for a key that is not set, and a default value
    Then: Return the default value
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    assert config.get_int("foo", 345) == 345


def test_get_int__key_value_is_set_to_invalid_type():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting an integer value for a key that is set to am invalid value
    Then: raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._merge({"box": "red"})

    with pytest.raises(
        ConfigurationError,
        match="Configuration key 'box' value cannot be returned as type 'int'",
    ):
        config.get_int("box")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0", False),
        ("true", True),
        ("False", False),
        ("True", True),
        ("", False),
        ("1", True),
        (1, True),
        ("foo", False),
    ],
)
def test_get_bool__key_value_is_set(value, expected):
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a boolean value for a key that is set
    Then: Return the boolean value for that key
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._merge({"bag": value})

    assert config.get_bool("bag") == expected


def test_get_bool__key_value_is_not_set_no_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a boolean value for a key that is not set, with no default value
    Then: raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    with pytest.raises(ConfigurationError, match="Configuration key 'foo' is not set"):
        config.get_bool("foo")


def test_get_bool__key_value_is_not_set_default_given():
    """
    Given: A `LeagueRankerConfig` instance
    When: Requesting a boolean value for a key that is not set, and a default value
    Then: Return the default value
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    assert config.get_bool("boo", True) is True
    assert config.get_bool("bot", False) is False


@pytest.fixture
def patched_environ(mocker):
    """Patch environment variables."""
    mocker.patch.dict(
        os.environ,
        {
            "RANKER_STRICT_PARSER": "true",
            "RANKER_points_win": "5",
            "RANKER_SUCCESS_MESSAGE": "Done",
        },
    )


def test_load_from_env(patched_environ):
    """
    Given: Correctly-prefixed environment variables are set
    When: Requesting the key from `LeagueRankerConfig`
    Then: The expected value is returned
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()

    assert config.get_bool("strict_parser") is True
    assert config.get_int("points_win", 5)
    assert config.get_str("success_message", "Done")


def test_load_from_env_immutable(patched_environ):
    """
    Given: Correctly-prefixed environment variables are set
    When: Setting the key value
    Then: The key value is immutable
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config.set("points_win", 15)

    assert config.get_int("points_win", 5)
