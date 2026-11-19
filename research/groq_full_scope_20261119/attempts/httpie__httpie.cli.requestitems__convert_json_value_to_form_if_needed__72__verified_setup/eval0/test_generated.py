import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.cli.exceptions import ParseError
from httpie.cli.argtypes import KeyValueArg


def test_in_json_mode_pass_through():
    """When in_json_mode is True, the returned function should be the original processor."""
    def processor(arg: KeyValueArg):
        return {"key": "value"}  # complex type

    wrapped = convert_json_value_to_form_if_needed(True, processor)
    # The wrapper should be the same callable as processor
    assert wrapped is processor
    # Calling it should return the complex dict unchanged
    result = wrapped()
    assert result == {"key": "value"}


def test_form_wrapper_primitive():
    """When not in JSON mode, primitive values are converted to strings."""
    def processor(arg: KeyValueArg):
        return 42  # primitive int

    wrapped = convert_json_value_to_form_if_needed(False, processor)
    # The wrapped function should return the string representation of the int
    assert wrapped() == "42"


def test_form_wrapper_complex_error_and_parse_error():
    """Complex values raise ParseError; processor raising ParseError yields None."""
    # Complex value case
    def complex_processor(arg: KeyValueArg):
        return [1, 2, 3]  # list is a complex type

    wrapped_complex = convert_json_value_to_form_if_needed(False, complex_processor)
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapped_complex()

    # Processor that raises ParseError
    def error_processor(arg: KeyValueArg):
        raise ParseError("invalid")

    wrapped_error = convert_json_value_to_form_if_needed(False, error_processor)
    # The wrapper should catch the ParseError and return None
    assert wrapped_error() is None
