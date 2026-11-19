import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.cli.exceptions import ParseError

def test_in_json_mode_returns_original_processor():
    # A processor that simply returns its argument
    def processor(arg):
        return arg

    wrapped = convert_json_value_to_form_if_needed(True, processor)
    # In JSON mode the wrapper should be the original processor
    assert wrapped is processor
    assert wrapped("value") == "value"

def test_non_json_mode_with_primitive_value_returns_string():
    # Processor that returns a primitive value
    def processor(arg):
        return 42

    wrapped = convert_json_value_to_form_if_needed(False, processor)
    # The wrapper should convert the primitive to a string
    assert wrapped("ignored") == "42"

def test_non_json_mode_with_complex_value_raises_parse_error():
    # Processor that returns a complex value (dict)
    def processor(arg):
        return {"key": "value"}

    wrapped = convert_json_value_to_form_if_needed(False, processor)
    # The wrapper should raise ParseError for complex types
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapped("ignored")
