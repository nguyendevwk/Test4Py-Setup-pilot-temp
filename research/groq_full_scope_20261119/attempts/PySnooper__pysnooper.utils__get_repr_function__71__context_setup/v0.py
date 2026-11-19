import builtins
import pytest
from pysnooper.utils import get_repr_function

def test_get_repr_function_matches_type_condition():
    # custom_repr contains a type condition that should match int
    custom_repr = [
        (int, lambda x: f"int:{x}"),
        (str, lambda x: f"str:{x}"),
    ]
    result = get_repr_function(42, custom_repr)
    assert result == "int:42"

def test_get_repr_function_falls_back_to_repr_when_no_match():
    # custom_repr contains conditions that do not match the item
    custom_repr = [
        (list, lambda x: f"list:{x}"),
        (dict, lambda x: f"dict:{x}"),
    ]
    result = get_repr_function(3.14, custom_repr)
    # Should use the built-in repr for a float
    assert result == repr(3.14)

def test_get_repr_function_handles_custom_callable_condition():
    # custom_repr uses a callable condition that checks for a specific attribute
    class Dummy:
        def __init__(self, value):
            self.value = value

    custom_repr = [
        (lambda x: hasattr(x, "value") and x.value > 10, lambda x: f"high:{x.value}"),
        (lambda x: hasattr(x, "value") and x.value <= 10, lambda x: f"low:{x.value}"),
    ]
    high = Dummy(15)
    low = Dummy(5)
    assert get_repr_function(high, custom_repr) == "high:15"
    assert get_repr_function(low, custom_repr) == "low:5"
