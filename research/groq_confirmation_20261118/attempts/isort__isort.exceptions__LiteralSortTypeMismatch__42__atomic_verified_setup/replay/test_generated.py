import pytest
from isort.exceptions import LiteralSortTypeMismatch, ISortError


def test_literal_sort_type_mismatch_message_and_attributes():
    """Verify that the exception message contains the expected type names
    and that the attributes are set correctly."""
    kind = int
    expected_kind = list
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should mention both the provided and expected types
    assert "int" in str(exc)
    assert "list" in str(exc)
    assert "isort was told to sort a literal of type" in str(exc)

    # Attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind


def test_literal_sort_type_mismatch_inherits_from_isort_error():
    """Ensure that LiteralSortTypeMismatch is a subclass of ISortError."""
    exc = LiteralSortTypeMismatch(str, dict)
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_literal_sort_type_mismatch_raises_with_invalid_arguments():
    """Confirm that constructing the exception with non-type arguments
    still creates an instance but the message reflects the actual objects."""
    kind = "not_a_type"
    expected_kind = 42
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should include the string representations of the arguments
    assert "not_a_type" in str(exc)
    assert "42" in str(exc)

    # Attributes should store the original objects
    assert exc.kind == kind
    assert exc.expected_kind == expected_kind
