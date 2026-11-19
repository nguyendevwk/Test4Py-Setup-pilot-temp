import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_with_integers():
    """All elements are integers – should return True."""
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_with_multiple_types():
    """Elements are either int or str – should return True."""
    seq = [1, "two", 3, "four"]
    assert validate_types_in_sequence(seq, (int, str)) is True

def test_validate_types_in_sequence_with_mixed_types():
    """Sequence contains a float – should return False."""
    seq = [1, 2.5, 3]
    assert validate_types_in_sequence(seq, int) is False
