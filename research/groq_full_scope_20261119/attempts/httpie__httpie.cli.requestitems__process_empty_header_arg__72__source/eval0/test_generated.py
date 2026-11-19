import pytest
from httpie.cli.requestitems import process_empty_header_arg
from httpie.exceptions import ParseError

class DummyArg:
    def __init__(self, orig, value):
        self.orig = orig
        self.value = value

def test_process_empty_header_arg_returns_empty_string():
    arg = DummyArg(orig="X-Test", value="")
    result = process_empty_header_arg(arg)
    assert result == "", "Expected empty string to be returned unchanged"

def test_process_empty_header_arg_returns_none_for_none_value():
    arg = DummyArg(orig="X-Test", value=None)
    result = process_empty_header_arg(arg)
    assert result is None, "Expected None to be returned unchanged"

def test_process_empty_header_arg_raises_on_non_empty_value():
    arg = DummyArg(orig="X-Test", value="not-empty")
    with pytest.raises(ParseError) as excinfo:
        process_empty_header_arg(arg)
    assert "Invalid item" in str(excinfo.value)
    assert arg.orig in str(excinfo.value)
