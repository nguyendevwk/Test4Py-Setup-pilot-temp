import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.cli.exceptions import ParseError


def test_in_json_mode_returns_original_processor():
    """When in_json_mode is True, the returned callable should be the original processor."""
    def dummy_processor(arg):
        return {"key": "value"}

    wrapped = convert_json_value_to_form_if_needed(True, dummy_processor)
    # The wrapped function should be the same object as dummy_processor
    assert wrapped is dummy_processor
    # Calling it should return the original value unchanged
    assert wrapped("anything") == {"key": "value"}


def test_non_json_mode_with_primitive_value():
    """When not in JSON mode, primitive values are converted to strings."""
    def primitive_processor(arg):
        # Return an integer; the wrapper should convert it to a string
        return 42

    wrapped = convert_json_value_to_form_if_needed(False, primitive_processor)
    # The wrapped function should return a string representation of the integer
    assert wrapped("ignored") == "42"


def test_non_json_mode_with_complex_value_or_error():
    """When not in JSON mode, complex values or ParseError raise ParseError."""
    # Processor that returns a complex type (dict)
    def complex_processor(arg):
        return {"a": 1}

    wrapped_complex = convert_json_value_to_form_if_needed(False, complex_processor)
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapped_complex("ignored")

    # Processor that raises ParseError
    def error_processor(arg):
        raise ParseError("original error")

    wrapped_error = convert_json_value_to_form_if_needed(False, error_processor)
    with pytest.raises(ParseError, match="original error"):
        wrapped_error("ignored")
