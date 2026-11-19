import pytest
from string_utils.validation import is_integer

def test_is_integer_normal_cases():
    # Typical integer strings
    assert is_integer("0") is True
    assert is_integer("-123") is True
    assert is_integer("+456") is True
    # Non-integer numeric formats
    assert is_integer("42.0") is False
    assert is_integer("1e3") is False  # scientific notation contains a dot
    assert is_integer("abc") is False

def test_is_integer_boundary_large_numbers():
    # Very large integer string
    large_int = "9" * 1000  # 1000-digit number
    assert is_integer(large_int) is True
    # Large number with decimal point should be False
    large_float = large_int + ".0"
    assert is_integer(large_float) is False

def test_is_integer_invalid_input_type():
    # Passing a non-string should raise a TypeError due to string operations
    with pytest.raises(TypeError):
        is_integer(None)
