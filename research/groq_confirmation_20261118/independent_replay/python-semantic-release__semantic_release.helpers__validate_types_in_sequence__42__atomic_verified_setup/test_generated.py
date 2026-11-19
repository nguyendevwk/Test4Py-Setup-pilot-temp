import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_all_correct():
    """All elements match the specified type – should return True."""
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_empty_sequence():
    """An empty sequence is considered valid for any type – should return True."""
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_validate_types_in_sequence_invalid_type_argument():
    """Passing a non-type as the 'types' argument should raise a TypeError."""
    seq = [1, 2, 3]
    with pytest.raises(TypeError):
        validate_types_in_sequence(seq, [int, str])  # list is not a valid type argument
