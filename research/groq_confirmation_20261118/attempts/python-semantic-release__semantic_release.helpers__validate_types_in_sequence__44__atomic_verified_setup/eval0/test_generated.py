import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_with_integers():
    """All elements are integers – should return True."""
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_with_multiple_types():
    """Sequence contains ints and strings – should return True when both types allowed."""
    seq = [1, "two", 3, "four"]
    assert validate_types_in_sequence(seq, (int, str)) is True

def test_validate_types_in_sequence_with_invalid_element():
    """Sequence contains a float – should return False when only ints allowed."""
    seq = [1, 2.5, 3]
    assert validate_types_in_sequence(seq, int) is False
