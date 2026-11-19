import pytest
from httpie.cli.requestitems import process_empty_header_arg
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.exceptions import ParseError


def test_process_empty_header_arg_returns_empty_value(tmp_path):
    """When the header argument has an empty value, the function should return that empty value."""
    # Create a KeyValueArg with an empty value
    arg = KeyValueArg(orig="Header;", value="")
    result = process_empty_header_arg(arg)
    assert result == ""  # The empty string is returned unchanged


def test_process_empty_header_arg_raises_on_non_empty_value(tmp_path):
    """When the header argument has a non‑empty value, a ParseError should be raised."""
    arg = KeyValueArg(orig="Header: value", value="value")
    with pytest.raises(ParseError) as excinfo:
        process_empty_header_arg(arg)
    # The error message should reference the original argument string
    assert "Header: value" in str(excinfo.value)
    assert "to specify an empty header" in str(excinfo.value)


def test_process_empty_header_arg_boundary_whitespace(tmp_path):
    """A header value that is only whitespace should be treated as non‑empty and raise an error."""
    arg = KeyValueArg(orig="Header:   ", value="   ")
    with pytest.raises(ParseError):
        process_empty_header_arg(arg)
