import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_with_integers():
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_with_mixed_and_tuple_of_types():
    seq = [1, "two", 3.0]
    # Accept int, str, or float
    assert validate_types_in_sequence(seq, (int, str, float)) is True
    # Reject if any element not in allowed types
    seq_bad = [1, "two", None]
    assert validate_types_in_sequence(seq_bad, (int, str, float)) is False

def test_validate_types_in_sequence_with_empty_and_string_sequence():
    # Empty sequence should return True
    assert validate_types_in_sequence([], int) is True
    # String is a sequence of characters; all are str
    assert validate_types_in_sequence("abc", str) is True
    # String with non-str elements cannot occur, but test that a non-string sequence fails
    assert validate_types_in_sequence([1, 2, 3], str) is False
