"""Unit test for the cli interface."""
import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner(valid_input_data):
    """Fixture patches reading input file argument."""
    runner = CliRunner()

    # Setup: Enter isolated filesystem context and create the input file
    with runner.isolated_filesystem():
        with open("foo.in", "w") as f:
            f.write(valid_input_data)

        yield runner


def test_cli__valid_input_path_given(mocker, valid_input_data):
    """
    Given: The cli is invoked with a file path argument
    When: The file path is valid
    Then: The command should return an exit code of 0.
    """
    from ranker.main import cli

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("foo.in", "w") as f:
            f.write(valid_input_data)

        result = runner.invoke(cli, ["foo.in"])

    assert result.exit_code == 0


def test_cli__invalid_input_path_given():
    """
    Given: The cli is invoked with a file path argument
    When: The file path is valid
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["var.in"])
    assert result.exit_code == 2
    assert "No such file or directory" in result.output


def test_cli__no_input_path_given():
    """
    Given: The cli is invoked
    When: No file path argument is specified
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 2
    assert " Missing argument 'INPUT'" in result.output


def test_cli__invalid_input_log_level_given(cli_runner):
    """
    Given: The cli is invoked with a `--log-level` argument
    When: The `--log-level` value is invalid
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    result = cli_runner.invoke(cli, ["foo.in", "--log-level", "FOO"])
    assert result.exit_code == 2
    assert "Invalid value for '--log-level' / '-l':" in result.output


def test_cli__verbose_flag_prints_stats(cli_runner):
    """
    Given: The cli is invoked with a valid file path argument
    When: The `--verbose` flag is set
    Then: The command should print a stats table.
    """
    from ranker.main import cli

    result = cli_runner.invoke(cli, ["foo.in", "--verbose"])
    assert result.exit_code == 0
    assert "Statistics:" in result.output


def test_cli__strict_flag_prints_note(cli_runner):
    """
    Given: The cli is invoked with a valid file input argument
    When: The `--strict` flag is set
    Then: The command should print a note.
    """
    from ranker.main import cli

    result = cli_runner.invoke(cli, ["foo.in", "--strict"])
    assert result.exit_code == 0
    assert "Note: Strict parsing is enabled." in result.output


def test_cli__log_level_default(cli_runner):
    """
    Given: The cli is invoked with a valid file path argument
    When: The `--log-level` flag is not set
    Then: The configuration log_level should be "ERROR"
    """
    from ranker.config import LeagueRankerConfig
    from ranker.main import cli

    result = cli_runner.invoke(cli, ["foo.in"])
    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("log_level") == "ERROR"


def test_cli__log_level_is_set(cli_runner):
    """
    Given: The cli is invoked with a valid file path argument
    When: The `--log-level` flag is set
    Then: The configuration log_level should be the selected level
    """
    from ranker.config import LeagueRankerConfig
    from ranker.main import cli

    result = cli_runner.invoke(cli, ["foo.in", "--log-level", "ERROR"])
    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("log_level") == "ERROR"


def test_cli__config_path_is_set(valid_input_data, config_yaml):
    """
    Given: The cli is invoked with a valid file path argument
    When: The `--config` path is valid
    Then: The configuration config_path value should be set
    """
    from ranker.config import LeagueRankerConfig
    from ranker.main import cli

    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("foo.in", "w") as f:
            f.write(valid_input_data)

        with open("var.yaml", "w") as f:
            f.write(config_yaml)

        result = runner.invoke(cli, ["foo.in", "--config", "var.yaml"])

    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("config_path") == "var.yaml"
