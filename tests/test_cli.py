"""Unit test for the cli interface."""

from click.testing import CliRunner


def test_cli__valid_input_arg_given():
    """
    Given: The cli is invoked with a `--input` argument
    When: The `--input` file path is valid
    Then: The command should return an exit code of 0.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/data.in"])
    assert result.exit_code == 0


def test_cli__invalid_input_arg_given():
    """
    Given: The cli is invoked with a `--input` argument
    When: The `--input` file path is invalid (the file does not exist)
    Then: The command should return an exit code of 2.
    """
    from ranker.main import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["--input", "data/foo.in"])
    assert result.exit_code == 2
    assert "Error: Invalid value for '--input': 'data/foo.in':" in result.output


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
