import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_all_ints_returns_true():
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_empty_sequence_returns_true():
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_validate_types_in_sequence_invalid_types_argument_raises():
    seq = [1, 2, 3]
    with pytest.raises(TypeError):
        validate_types_in_sequence(seq, [int, str])
