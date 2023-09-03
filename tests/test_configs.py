"""Unit tests for the ranker.configs module."""
import os
import re

import pytest

from ranker.errors import ConfigurationError


@pytest.fixture
def config(mocker, config_yaml):
    """
    Disable the `config` auto fixture for these tests.

    See `tests/conftest.py`
    """
    mocker.patch("builtins.open", mocker.mock_open(read_data=config_yaml))


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
        (False, False),
        ("True", True),
        (True, True),
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


def test_load_from_file__file_does_not_exist(mocker):
    """
    Given: Reading a YAML file path
    When: The given file does not exist
    Then: Raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    mocker.patch("builtins.open", side_effect=FileNotFoundError())

    with pytest.raises(
        ConfigurationError, match="Could not read from file '/var/foo/bar.yaml'"
    ):
        LeagueRankerConfig()


def test__find_config_path__file_exists_at_path(mocker):
    """
    Given: Finding a YAML config file
    When: A valid file is found
    Then: Load that file
    """
    mocker.patch("os.path.isfile", return_value=True)

    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._config_dirs = ["/foo/bar"]
    config._data.pop("config_path")

    assert config._find_config_path() == "/foo/bar/league-ranker.yaml"


def test__find_config_path__no_file_at_path():
    """
    Given: Finding a YAML config file
    When: No file can be found
    Then: Raise a `ConfigurationError` exception
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._config_dirs = ["/foo/bar"]
    config._data.pop("config_path")

    with pytest.raises(
        ConfigurationError,
        match=re.escape("No configuration file found in ['/foo/bar']"),
    ):
        config._find_config_path()


def test__find_config_path__config_path_is_set():
    """
    Given: Finding a YAML config file
    When: config_path is set
    Then: return config_path
    """
    from ranker.configs import LeagueRankerConfig

    config = LeagueRankerConfig()
    config._data["config_path"] = "/foo/bar"

    assert config._find_config_path() == "/foo/bar"
