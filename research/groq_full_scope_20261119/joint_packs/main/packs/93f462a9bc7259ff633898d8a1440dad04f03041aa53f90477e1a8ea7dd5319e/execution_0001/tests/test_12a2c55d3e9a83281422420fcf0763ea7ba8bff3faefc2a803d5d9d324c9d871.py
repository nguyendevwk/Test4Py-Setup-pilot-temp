import pytest
from httpie.cli.requestitems import convert_json_value_to_form_if_needed
from httpie.cli.exceptions import ParseError
from httpie.cli.argtypes import KeyValueArg

# Helper processor that records its arguments and returns a value or raises ParseError
class DummyProcessor:
    def __init__(self, return_value=None, raise_error=False):
        self.return_value = return_value
        self.raise_error = raise_error
        self.called_with = None

    def __call__(self, *args, **kwargs):
        self.called_with = (args, kwargs)
        if self.raise_error:
            raise ParseError("dummy error")
        return self.return_value

def test_primitive_value_is_converted_to_string():
    """When not in JSON mode, primitive values are converted to string."""
    processor = DummyProcessor(return_value=42)
    wrapped = convert_json_value_to_form_if_needed(False, processor)
    result = wrapped()
    assert result == "42"
    assert processor.called_with == ((), {})

def test_complex_value_raises_parse_error():
    """Complex values (e.g., dict) raise ParseError when not in JSON mode."""
    processor = DummyProcessor(return_value={"a": 1})
    wrapped = convert_json_value_to_form_if_needed(False, processor)
    with pytest.raises(ParseError, match="Cannot use complex JSON value types"):
        wrapped()

def test_json_mode_passes_through_processor():
    """When in JSON mode, the processor is returned unchanged."""
    processor = DummyProcessor(return_value=[1, 2, 3])
    wrapped = convert_json_value_to_form_if_needed(True, processor)
    # The returned callable should be the original processor
    assert wrapped is processor
    result = wrapped()
    assert result == [1, 2, 3]
