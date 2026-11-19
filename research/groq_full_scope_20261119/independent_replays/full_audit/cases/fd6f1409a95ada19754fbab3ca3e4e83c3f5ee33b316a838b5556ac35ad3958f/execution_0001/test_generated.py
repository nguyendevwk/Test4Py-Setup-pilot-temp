import builtins
import pytest
from pysnooper.utils import get_repr_function

def test_get_repr_function_matches_type_condition():
    # custom_repr contains a type condition that should match int
    custom_repr = [
        (int, lambda x: f"int:{x}"),
        (str, lambda x: f"str:{x}"),
    ]
    result_func = get_repr_function(42, custom_repr)
    assert result_func(42) == "int:42"
    # Ensure that the function returned is the correct lambda
    assert result_func is custom_repr[0][1]

def test_get_repr_function_fallback_to_repr_when_no_match():
    # custom_repr contains conditions that do not match the item
    custom_repr = [
        (list, lambda x: f"list:{x}"),
        (dict, lambda x: f"dict:{x}"),
    ]
    result_func = get_repr_function("hello", custom_repr)
    # Since no condition matches, the function should be the built-in repr
    assert result_func is builtins.repr
    assert result_func("hello") == "'hello'"

def test_get_repr_function_handles_lambda_condition_and_order():
    # custom_repr contains a lambda that matches any string starting with 'a'
    custom_repr = [
        (lambda x: isinstance(x, str) and x.startswith('a'), lambda x: f"starts-with-a:{x}"),
        (str, lambda x: f"str:{x}"),
    ]
    # The first condition should match and be used
    result_func = get_repr_function("apple", custom_repr)
    assert result_func("apple") == "starts-with-a:apple"
    # A string that does not start with 'a' should fall back to the second condition
    result_func = get_repr_function("banana", custom_repr)
    assert result_func("banana") == "str:banana"
