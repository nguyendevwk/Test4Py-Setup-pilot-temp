import pytest
from string_utils.validation import is_integer

def test_is_integer_normal_cases():
    """Verify that typical integer strings are accepted and non‑integers are rejected."""
    assert is_integer("0") is True
    assert is_integer("-123") is True
    assert is_integer("+987654321") is True
    assert is_integer("42.0") is False
    assert is_integer("3.14") is False
    assert is_integer("1e3") is False  # scientific notation is not an integer string

def test_is_integer_boundary_large_numbers():
    """Check that very large integer strings are handled correctly."""
    large_int = "9" * 1000  # 1000 digits
    assert is_integer(large_int) is True
    # Adding a decimal point should invalidate it
    assert is_integer(large_int + ".0") is False

def test_is_integer_invalid_input_type():
    """Passing a non‑string should raise a TypeError."""
    with pytest.raises(TypeError):
        is_integer(123)  # type: ignore[arg-type]
