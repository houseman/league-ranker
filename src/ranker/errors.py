"""Exception classes."""


class ConfigurationError(Exception):
    """Raise when a configuration error is encountered."""

    pass


class RecordParseError(Exception):
    """Input data record could not be parsed."""

    pass
