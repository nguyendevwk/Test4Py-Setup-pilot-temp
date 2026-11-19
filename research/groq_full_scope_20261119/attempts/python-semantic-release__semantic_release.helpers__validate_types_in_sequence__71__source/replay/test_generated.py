import pytest
from semantic_release.helpers import validate_types_in_sequence


def test_validate_types_in_sequence_normal():
    """Normal case: all elements match the expected type."""
    seq = [1, 2, 3]
    assert validate_types_in_sequence(seq, int) is True
    # Mixed types should return False
    mixed_seq = [1, "two", 3]
    assert validate_types_in_sequence(mixed_seq, int) is False
    # Using a tuple of types
    assert validate_types_in_sequence(mixed_seq, (int, str)) is True


def test_validate_types_in_sequence_boundary():
    """Boundary case: empty sequence should return True."""
    empty_seq = []
    assert validate_types_in_sequence(empty_seq, int) is True
    # Sequence with one element of correct type
    single = [42]
    assert validate_types_in_sequence(single, int) is True
    # Sequence with one element of incorrect type
    single_wrong = ["hello"]
    assert validate_types_in_sequence(single_wrong, int) is False


def test_validate_types_in_sequence_error():
    """Error case: passing a non‑iterable should raise TypeError."""
    with pytest.raises(TypeError):
        validate_types_in_sequence(42, int)
