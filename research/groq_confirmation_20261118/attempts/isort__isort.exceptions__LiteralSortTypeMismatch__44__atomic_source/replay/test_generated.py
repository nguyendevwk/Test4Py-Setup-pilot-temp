import pytest
from isort.exceptions import LiteralSortTypeMismatch, ISortError


def test_literal_sort_type_mismatch_message_and_attributes():
    """Verify that the exception message contains the expected type names and that
    the `kind` and `expected_kind` attributes are set correctly."""
    # Use built-in types to avoid importing custom classes
    kind = list
    expected_kind = dict
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should mention both type names
    assert "list" in str(exc)
    assert "dict" in str(exc)

    # The attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind


def test_literal_sort_type_mismatch_inherits_from_isort_error():
    """Ensure that LiteralSortTypeMismatch is a subclass of ISortError."""
    exc = LiteralSortTypeMismatch(int, str)
    # ISortError is the base exception for isort
    assert isinstance(exc, ISortError)


def test_literal_sort_type_mismatch_raises_and_catches():
    """Test that the exception can be raised and caught, and that the caught
    exception preserves its message and attributes."""
    with pytest.raises(LiteralSortTypeMismatch) as excinfo:
        raise LiteralSortTypeMismatch(tuple, set)

    # The caught exception should have the same attributes
    caught = excinfo.value
    assert caught.kind is tuple
    assert caught.expected_kind is set
    # The message should be correctly formatted
    assert "tuple" in str(caught)
    assert "set" in str(caught)
