# League Ranker
A command-line application that will calculate the ranking table for a league

## Download
> **Note**
> This package is intentionally *not* available on Pypi.

Clone the repository
1. Use `git clone`
```shell
❯ git clone git@github.com:houseman/league-ranker.git
```
2. Change into the source directory
```
❯ cd league-ranker
```

## Installation
> **Important**
> It is strongly advised that you create and use a Python virtual environment.

> **Important**
> This package requires *Python >= 3.11*

1. Create a Python virtual environment
```shell
❯ python3.11 -m venv venv
```
2. Activate the the environment
```shell
❯ source ./venv/bin/activate
```
3. Use `pip` to install the package
```shell
❯ pip install .
```
## Usage
When correctly installed, League Ranker will make the `rank` command available to you.

Run this with the `--help` option to learn more about usage.

```shell
❯ rank --help
Usage: rank [OPTIONS] INPUT

  Calculate and print the ranking table for a league.

  INPUT should be a input file path, or '-' for stdin.

Options:
  -c, --config FILE               Path to a configuration file
  -s, --strict                    Enable strict parsing. Input values will not
                                  be normalised.
  -v, --verbose                   Run verbosely (prints statistics at
                                  completion).
  -l, --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Sets the logger level.
  --help                          Show this message and exit.
```

### Input
A path to an input data file is required at minimum:
```shell
❯ rank data/data.in

1. Tarantulas, 6 pts
2. Lions, 5 pts
3. FC Awesome, 1 pt
3. Snakes, 1 pt
5. Grouches, 0 pts
```

It is possible to read from stdin too (using redirection):
```shell
❯ cat data/data.in | rank -

1. ...
```

### Strict Parsing
The parser will attempt to normalise input data that may be badly-formatted.

These normalisations are:
- Strip all characters that are not alphanumeric, space or comma
- Replace underscores with spaces
- Reduce consecutive spaces to a single space
- Strip leading and trailing spaces

> **Important**
> The default `rank` behaviour is for *strict parsing* to be **disabled**.

If you wish to *enable* strict parsing, use the `--strict` or `-s` option.
A note will be printed when strict parsing is enabled.
```shell
❯ rank data/data.in --strict

Note: Strict parsing is enabled.

1. ...
```

### Verbosity
Use the `--verbose` or `-v` option to increase `rank` verbosity.

Doing so will enable printing of statistics at completion.
```shell
❯ rank data/data.in --verbose

1. ...


Statistics:
╒════════════╤═════════════╤══════════╕
│   Imported │   Processed │   Failed │
╞════════════╪═════════════╪══════════╡
│          5 │           5 │        0 │
╘════════════╧═════════════╧══════════╛
```

### Log level
The default log level is `ERROR`, i.e. only errors will be logged to output.

This can be adjusted using the `--log-level` or `-l` option:
```shell
❯ rank data/data.in --log-level INFO
2023-09-04 11:21:46,257 - INFO - Read config from file ...
```
### Configuration file
Configurations are persisted in a [YAML file](src/league-ranker.yaml).

The `rank` cli will look for this configuration file at the following locations, in the listed order:
1. The current working directory (`./league-ranker.yaml`)
2. A `.ranker` directory within the user's home directory i.e. `~/.ranker/league-ranker.yaml`
3. The `league-ranker` package  in the `site-packages`` directory directory (bundled, this will be used by default)

This config file location can be over ridden using the `--config`/`-c` option. For example:
```shell
❯ cp src/ranker/league-ranker.yaml /tmp
❯ rank data/data.in --config /tmp/league-ranker.yaml -l INFO
2023-09-04 11:22:59,540 - INFO - Read config from file /tmp/league-ranker.yaml
...
```
## Configuration
As mentioned above, configuration is stored in a YAML file, which may be specified.

It is also possible to set configuration values using environment variables. For example:
```shell
❯ RANKER_STRICT_PARSE=true rank data/data.in

Note: Strict parsing is enabled.

1. ...
```

These environment variable names correspond to those in the YAML configuration file with the name in UPPERCASE, prefixed by `RANKER_`.

| YAML | ENV | Default |
| ---- | --- | ------- |
| `config.log_level` | `RANKER_LOG_LEVEL` | `ERROR` |
| `config.strict_parse` | `RANKER_STRICT_PARSE` | `False` |
| `config.verbose` | `RANKER_VERBOSE` | `False` |
| `config.points_win` | `RANKER_POINTS_WIN` | `3` |
| `config.points_loss` | `RANKER_POINTS_LOSS` | `0` |
| `config.points_draw` | `RANKER_POINTS_DRAW` | `1` |

> **Important**
> *There is precedence* to these configuration sources. From highest to lowest priority:
> 1. Command line options (supersede)
> 2. Environment variables (supersede)
> 3. Configuration file

## Developer Notes
### Using `make`
A `Makefile` is available for the convenience of developers:
```
❯ make help
help                 Show this help message
install              Install project
lint                 Run linters
test                 Run tests
tool                 Install development tools
```
### Installation
To install the required development tools, run:
```shell
❯ python -m pip install  --editable ".[dev]"
```
> **Note**
> `make tool` will do the above for you.

### Linting
The following linting tools are used, and can be run through `make lint`:
- `black` code formatter
- `ruff` linter
- `mypy` type checker

### `pre-commit` hooks
Please do use the helpful `pre-commit` hooks before committing any changes.
```shell
❯ pre-commit install
❯ pre-commit run
```

### Unit tests
Unit test coverage is 100%. To run unit tests, use the `test` target.
```
❯ make test
```
or, simply run
```shell
❯ pytest
```
Coverage data is generated, and can be found in `htmlcov/index.html`.

## Test data
The file [`data/rwc_2019.in`](data/rwc_2019.in) contains input data from Rugby World Cup 2019.
Below are results,  adjusted to 4 points for a win and 2 points for a draw:
```shell
❯ RANKER_POINTS_WIN=4 RANKER_POINTS_DRAW=2 rank data/rwc_2019.in -v

1. Japan, 16 pts
1. Wales, 16 pts
3. England, 14 pts
3. France, 14 pts
3. New Zealand, 14 pts
6. Australia, 12 pts
6. Ireland, 12 pts
6. South Africa, 12 pts
9. Italy, 10 pts
10. Argentina, 8 pts
10. Scotland, 8 pts
12. Fiji, 4 pts
12. Georgia, 4 pts
12. Samoa, 4 pts
12. Tonga, 4 pts
12. Uruguay, 4 pts
17. Canada, 2 pts
17. Namibia, 2 pts
19. Russia, 0 pts
19. United States, 0 pts


Statistics:
╒════════════╤═════════════╤══════════╕
│   Imported │   Processed │   Failed │
╞════════════╪═════════════╪══════════╡
│         52 │          40 │       12 │
╘════════════╧═════════════╧══════════╛
```
_* Failed records are expected (have a look at the input file to see why)._
