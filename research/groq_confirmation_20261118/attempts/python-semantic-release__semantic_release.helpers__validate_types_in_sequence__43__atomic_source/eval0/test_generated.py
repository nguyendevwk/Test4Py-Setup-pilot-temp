import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_with_empty_sequence():
    """An empty sequence should return True."""
    assert validate_types_in_sequence([], int) is True

def test_validate_types_in_sequence_with_multiple_types():
    """Sequence elements should be validated against a tuple of types."""
    seq = [1, "two", 3.0]
    # All elements are either int, str, or float
    assert validate_types_in_sequence(seq, (int, str, float)) is True
    # If any element is not in the allowed types, validation fails
    seq.append(True)  # bool is not in the tuple
    assert validate_types_in_sequence(seq, (int, str, float)) is False

def test_validate_types_in_sequence_with_invalid_input():
    """Passing a non-iterable should raise a TypeError."""
    with pytest.raises(TypeError):
        validate_types_in_sequence(None, int)
