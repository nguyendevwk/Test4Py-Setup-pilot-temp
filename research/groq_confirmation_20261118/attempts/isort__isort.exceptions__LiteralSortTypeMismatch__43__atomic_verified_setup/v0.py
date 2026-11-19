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

    # The attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

def test_literal_sort_type_mismatch_inherits_from_isort_error():
    """Ensure that LiteralSortTypeMismatch is a subclass of ISortError."""
    kind = dict
    expected_kind = tuple
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # ISortError is the base class for all isort errors
    assert isinstance(exc, ISortError)
    # It should also be a standard Exception
    assert isinstance(exc, Exception)

def test_literal_sort_type_mismatch_with_subclass_and_same_type():
    """Test that passing a subclass of the expected type still works
    and that the message reflects the actual subclass."""
    class CustomList(list):
        pass

    kind = CustomList
    expected_kind = list
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should refer to the subclass name
    assert "CustomList" in str(exc)
    # The attributes should be the exact objects passed
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind
