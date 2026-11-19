import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_all_same_type_returns_true():
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_empty_sequence_returns_true():
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_validate_mixed_types_returns_false():
    seq = [1, "two", 3.0]
    assert validate_types_in_sequence(seq, (int, float)) is False
