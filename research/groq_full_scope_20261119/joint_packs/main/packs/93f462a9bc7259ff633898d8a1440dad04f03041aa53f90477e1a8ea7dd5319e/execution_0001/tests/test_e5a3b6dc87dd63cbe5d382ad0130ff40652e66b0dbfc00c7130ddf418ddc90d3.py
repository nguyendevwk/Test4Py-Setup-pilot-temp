import pytest
from httpie.cli.requestitems import process_empty_header_arg, ParseError

class DummyArg:
    def __init__(self, value, orig):
        self.value = value
        self.orig = orig

def test_returns_empty_string_when_value_is_empty():
    arg = DummyArg(value="", orig="Header;")
    result = process_empty_header_arg(arg)
    assert result == ""

def test_raises_parse_error_when_value_is_non_empty():
    arg = DummyArg(value="Content-Type: application/json", orig="Header;")
    with pytest.raises(ParseError) as excinfo:
        process_empty_header_arg(arg)
    assert "Invalid item" in str(excinfo.value)
    assert arg.orig in str(excinfo.value)

def test_error_message_contains_original_argument():
    arg = DummyArg(value="X-Test: 123", orig="X-Test: 123")
    with pytest.raises(ParseError) as excinfo:
        process_empty_header_arg(arg)
    assert str(excinfo.value).startswith("Invalid item")
    assert arg.orig in str(excinfo.value)
