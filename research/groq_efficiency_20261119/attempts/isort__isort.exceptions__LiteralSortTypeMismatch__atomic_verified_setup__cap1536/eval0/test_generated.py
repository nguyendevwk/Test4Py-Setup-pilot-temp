import pytest
from isort.exceptions import LiteralSortTypeMismatch
from isort.exceptions import ISortError


def test_literal_sort_type_mismatch_message_and_attributes():
    """Verify that the exception message contains the expected type names
    and that the attributes are set correctly."""
    kind = int
    expected_kind = list
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should mention both types
    assert "int" in str(exc)
    assert "list" in str(exc)

    # Attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind


def test_literal_sort_type_mismatch_inherits_isort_error():
    """Ensure that LiteralSortTypeMismatch is a subclass of ISortError."""
    kind = dict
    expected_kind = tuple
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # ISortError should be in the MRO
    assert isinstance(exc, ISortError)
    # Also a generic Exception
    assert isinstance(exc, Exception)


def test_literal_sort_type_mismatch_raises_with_invalid_arguments():
    """Confirm that passing non-type arguments raises a TypeError during construction."""
    with pytest.raises(TypeError):
        # The constructor expects type objects; passing a string should fail
        LiteralSortTypeMismatch("not_a_type", list)
