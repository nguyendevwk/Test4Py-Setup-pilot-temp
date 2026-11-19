import pytest
from pysnooper.utils import get_repr_function

def test_get_repr_function_with_type_condition(tmp_path):
    # Custom representation for int type
    custom_repr = [
        (int, lambda x: f"int:{x}"),
    ]
    # Should return the custom lambda for an int
    repr_func = get_repr_function(42, custom_repr)
    assert repr_func(42) == "int:42"
    # Non-int should fall back to default repr
    repr_func_default = get_repr_function("hello", custom_repr)
    assert repr_func_default("hello") == repr("hello")

def test_get_repr_function_with_callable_condition(tmp_path):
    # Custom representation for strings longer than 5 characters
    custom_repr = [
        (lambda x: isinstance(x, str) and len(x) > 5, lambda x: f"long:{x}"),
    ]
    # Should use custom lambda for long string
    repr_func = get_repr_function("abcdefg", custom_repr)
    assert repr_func("abcdefg") == "long:abcdefg"
    # Short string should use default repr
    repr_func_default = get_repr_function("abc", custom_repr)
    assert repr_func_default("abc") == repr("abc")

def test_get_repr_function_with_invalid_condition_raises(tmp_path):
    # Condition is not callable; should raise TypeError when called
    custom_repr = [
        ("not a callable", lambda x: f"invalid:{x}"),
    ]
    with pytest.raises(TypeError):
        get_repr_function(10, custom_repr)
