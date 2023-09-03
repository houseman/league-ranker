"""Unit test for the cli interface."""

from click.testing import CliRunner


def test_cli__valid_input_path_given():
    """
    Given: The cli is invoked with a `--input` argument
    When: The `--input` file path is valid
    Then: The command should return an exit code of 0.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/data.in"])
    assert result.exit_code == 0


def test_cli__invalid_input_path_given():
    """
    Given: The cli is invoked with a `--input` argument
    When: The `--input` file path is invalid (the file does not exist)
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/foo.in"])
    assert result.exit_code == 2
    assert "Invalid value for '--input' / '-i':" in result.output


def test_cli__invalid_input_log_level_given():
    """
    Given: The cli is invoked with a `--log-level` argument
    When: The `--log-level` value is invalid
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/data.in", "--log-level", "FOO"])
    assert result.exit_code == 2
    assert "Invalid value for '--log-level' / '-l':" in result.output


def test_cli__valid_stdin_given():
    """
    Given: The cli is invoked with no argument
    When: Valid data is passed as input through STDIN
    Then: The command should return an exit code of 0.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, input="Lions 1, FC Awesome 1\n")
    assert result.exit_code == 0


def test_cli__verbose_flag_prints_stats():
    """
    Given: The cli is invoked with a valid `--input` argument
    When: The `--verbose` flag is set
    Then: The command should print a stats table.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/data.in", "--verbose"])
    assert result.exit_code == 0
    assert "Statistics:" in result.output


def test_cli__strict_flag_prints_note():
    """
    Given: The cli is invoked with a valid `--input` argument
    When: The `--strict` flag is set
    Then: The command should print a note.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/data.in", "--strict"])
    assert result.exit_code == 0
    assert "Note: Strict parsing is enabled." in result.output


def test_cli__log_level_default():
    """
    Given: The cli is invoked with a valid `--input` argument
    When: The `--log-level` flag is not set
    Then: The configuration log_level should be "INFO"
    """
    from ranker.configs import LeagueRankerConfig
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input", "data/data.in"],
    )
    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("log_level") == "INFO"


def test_cli__log_level_is_set():
    """
    Given: The cli is invoked with a valid `--input` argument
    When: The `--log-level` flag is set
    Then: The configuration log_level should be the selected level
    """
    from ranker.configs import LeagueRankerConfig
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input", "data/data.in", "--log-level", "ERROR"],
    )
    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("log_level") == "ERROR"


def test_cli__config_path_is_set():
    """
    Given: The cli is invoked with a valid `--config` argument
    When: The `--config` path is valid
    Then: The configuration config_path value should be set
    """
    from ranker.configs import LeagueRankerConfig
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["--input", "data/data.in", "--config", "src/league-ranker.yaml"],
    )
    assert result.exit_code == 0
    assert LeagueRankerConfig().get_str("config_path") == "src/league-ranker.yaml"
