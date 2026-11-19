import pytest
from semantic_release.helpers import validate_types_in_sequence

def test_validate_types_in_sequence_all_correct():
    """All elements are of the expected type – should return True."""
    seq = [1, 2, 3, 4]
    assert validate_types_in_sequence(seq, int) is True

def test_validate_types_in_sequence_empty_sequence():
    """An empty sequence should be considered valid for any type."""
    seq = []
    assert validate_types_in_sequence(seq, str) is True

def test_validate_types_in_sequence_invalid_type_raises():
    """Passing a non‑sequence should raise a TypeError when iterated over."""
    with pytest.raises(TypeError):
        validate_types_in_sequence(None, int)
