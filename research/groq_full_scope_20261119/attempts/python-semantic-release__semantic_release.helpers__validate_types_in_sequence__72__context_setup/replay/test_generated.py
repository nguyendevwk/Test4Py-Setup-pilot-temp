import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_all_ints():
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_empty_sequence():
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_validate_types_in_sequence_mixed_types():
    seq = [1, "two", 3.0]
    assert validate_types_in_sequence(seq, (int, float)) is False
