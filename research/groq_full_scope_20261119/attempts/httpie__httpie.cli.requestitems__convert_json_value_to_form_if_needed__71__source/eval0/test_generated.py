import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.exceptions import ParseError


def dummy_processor(value):
    """Simple processor that returns the value unchanged."""
    return value


def test_json_mode_returns_original_processor():
    """When in_json_mode is True, the returned callable is the original processor."""
    wrapped = convert_json_value_to_form_if_needed(True, dummy_processor)
    assert wrapped is dummy_processor
    assert wrapped("hello") == "hello"


def test_non_json_mode_with_primitive_value():
    """When not in JSON mode, primitive values are converted to strings."""
    wrapped = convert_json_value_to_form_if_needed(False, dummy_processor)
    assert wrapped(42) == "42"
    assert wrapped(3.14) == "3.14"
    assert wrapped("text") == "text"


def test_non_json_mode_with_complex_value_raises():
    """When not in JSON mode, complex values raise ParseError."""
    def complex_processor(_):
        return {"key": "value"}  # dict is a complex type

    wrapped = convert_json_value_to_form_if_needed(False, complex_processor)
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapped("ignored")
