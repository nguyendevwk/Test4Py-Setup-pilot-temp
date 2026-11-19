import pytest
from isort.exceptions import LiteralSortTypeMismatch, ISortError


def test_literal_sort_type_mismatch_initialization():
    """Verify that the exception stores the provided types and formats the message correctly."""
    kind = int
    expected_kind = list
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should mention both types
    assert "int" in str(exc)
    assert "list" in str(exc)

    # The attributes should be set to the exact objects passed
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind


def test_literal_sort_type_mismatch_is_subclass_of_isort_error():
    """Ensure the exception is a subclass of ISortError and behaves like a normal exception."""
    kind = dict
    expected_kind = tuple
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # ISortError is the base class
    assert isinstance(exc, ISortError)

    # The exception can be raised and caught normally
    with pytest.raises(LiteralSortTypeMismatch) as cm:
        raise exc
    assert cm.value is exc


def test_literal_sort_type_mismatch_message_consistency():
    """Check that the message remains consistent across multiple string conversions."""
    kind = str
    expected_kind = set
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    first_str = str(exc)
    second_str = exc.__repr__()
    third_str = exc.args[0]

    # All representations should be identical
    assert first_str == second_str == third_str
