import builtins
import pytest
from pysnooper.utils import get_repr_function

def test_get_repr_function_matches_type_condition():
    # Custom representation for int type
    custom_repr = [
        (int, lambda x: f"int:{x}"),
        (str, lambda x: f"str:{x}")
    ]
    result = get_repr_function(42, custom_repr)
    assert result == "int:42"

def test_get_repr_function_matches_callable_condition():
    # Condition is a callable that matches only even numbers
    custom_repr = [
        (lambda x: isinstance(x, int) and x % 2 == 0, lambda x: f"even:{x}"),
        (lambda x: isinstance(x, int), lambda x: f"int:{x}")
    ]
    result_even = get_repr_function(8, custom_repr)
    result_odd = get_repr_function(7, custom_repr)
    assert result_even == "even:8"
    assert result_odd == "int:7"

def test_get_repr_function_falls_back_to_repr():
    # No matching condition; should return built-in repr
    custom_repr = [
        (str, lambda x: f"str:{x}")
    ]
    obj = object()
    result = get_repr_function(obj, custom_repr)
    assert result == repr(obj)
