import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.exceptions import ParseError

# Dummy processor that simply returns the provided value or raises ParseError
def dummy_processor(value):
    if value == "raise":
        raise ParseError("dummy error")
    return value

def test_in_json_mode_returns_processor_directly():
    """When in_json_mode is True, the returned callable should be the original processor."""
    wrapper = convert_json_value_to_form_if_needed(True, dummy_processor)
    # The wrapper should be the same object as dummy_processor
    assert wrapper is dummy_processor
    # Calling it should behave exactly like the original
    assert wrapper("hello") == "hello"
    assert wrapper(123) == 123

def test_non_json_mode_converts_primitives_and_errors_on_complex():
    """When not in JSON mode, primitives are converted to strings; complex types raise ParseError."""
    wrapper = convert_json_value_to_form_if_needed(False, dummy_processor)

    # Primitive types are converted to strings
    assert wrapper("text") == "text"
    assert wrapper(42) == "42"
    assert wrapper(3.14) == "3.14"

    # Complex types (dict, list) should raise ParseError
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapper({"key": "value"})
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapper([1, 2, 3])

def test_non_json_mode_propagates_parse_error_from_processor():
    """If the underlying processor raises ParseError, it should be propagated unchanged."""
    wrapper = convert_json_value_to_form_if_needed(False, dummy_processor)
    with pytest.raises(ParseError, match="dummy error"):
        wrapper("raise")
