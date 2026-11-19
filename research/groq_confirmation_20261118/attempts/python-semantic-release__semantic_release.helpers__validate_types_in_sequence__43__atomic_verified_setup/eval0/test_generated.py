import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_with_empty_sequence():
    """An empty sequence should return True."""
    assert validate_types_in_sequence([], int) is True
    assert validate_types_in_sequence((), str) is True

def test_validate_types_in_sequence_with_multiple_allowed_types():
    """Elements should be validated against a tuple of allowed types."""
    seq = [1, "two", 3.0]
    # Allow int, str, float
    assert validate_types_in_sequence(seq, (int, str, float)) is True
    # Disallow one of the types
    assert validate_types_in_sequence(seq, (int, str)) is False

def test_validate_types_in_sequence_with_invalid_input_raises():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        validate_types_in_sequence(None, int)
