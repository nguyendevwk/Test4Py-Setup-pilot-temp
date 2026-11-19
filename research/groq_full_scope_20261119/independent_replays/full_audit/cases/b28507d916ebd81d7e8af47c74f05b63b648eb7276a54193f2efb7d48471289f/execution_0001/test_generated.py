import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_all_elements_of_same_type_returns_true():
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_empty_sequence_returns_true():
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_mixed_types_and_multiple_allowed_types_returns_false():
    seq = [1, "two", 3.0, "four"]
    # Allow int or str, but float should cause failure
    assert validate_types_in_sequence(seq, (int, str)) is False
