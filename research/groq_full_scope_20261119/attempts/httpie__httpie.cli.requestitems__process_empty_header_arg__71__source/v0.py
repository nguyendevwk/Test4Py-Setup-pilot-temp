import pytest
from httpie.cli.requestitems import process_empty_header_arg
from httpie.cli.argtypes import KeyValueArg
from httpie.cli.exceptions import ParseError

def test_empty_header_returns_value():
    """When the header value is an empty string, the function returns it unchanged."""
    arg = KeyValueArg(orig="Header;", value="")
    result = process_empty_header_arg(arg)
    assert result == ""

def test_non_empty_header_raises_parse_error():
    """When the header value is non‑empty, a ParseError is raised."""
    arg = KeyValueArg(orig="Header: value", value="value")
    with pytest.raises(ParseError):
        process_empty_header_arg(arg)

def test_error_message_contains_original_argument():
    """The ParseError message should include the original argument string."""
    arg = KeyValueArg(orig="X-Custom: data", value="data")
    with pytest.raises(ParseError) as excinfo:
        process_empty_header_arg(arg)
    assert "X-Custom: data" in str(excinfo.value)
