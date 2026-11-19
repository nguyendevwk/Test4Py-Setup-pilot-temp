import pytest
from string_utils.validation import is_integer

def test_is_integer_normal_cases():
    # Typical integer strings
    assert is_integer("0") is True
    assert is_integer("-123") is True
    assert is_integer("+456") is True
    # Non-integer numeric formats
    assert is_integer("42.0") is False
    assert is_integer("1e3") is False  # scientific notation contains 'e', not a dot
    assert is_integer("1.23e4") is False

def test_is_integer_boundary_and_large_numbers(tmp_path):
    # Very large integer string
    large_int = "9" * 1000  # 1000-digit number
    assert is_integer(large_int) is True
    # Scientific notation with large exponent
    sci_notation = "1e1000"
    assert is_integer(sci_notation) is False
    # Leading/trailing spaces should be considered invalid
    assert is_integer(" 42") is False
    assert is_integer("42 ") is False

def test_is_integer_invalid_input_type():
    # Passing a non-string should raise a TypeError
    with pytest.raises(TypeError):
        is_integer(42)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        is_integer(None)  # type: ignore[arg-type]
