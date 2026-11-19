import pytest
from isort.exceptions import LiteralSortTypeMismatch
from typing import List

def test_literal_sort_type_mismatch_message_and_attributes():
    """Verify that the exception message contains the provided type names
    and that the attributes are stored correctly."""
    kind = int
    expected_kind = List
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # The message should mention both type names
    assert "int" in str(exc)
    assert "typing.List" in str(exc)
    # Attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

def test_literal_sort_type_mismatch_inherits_from_exception():
    """Ensure that LiteralSortTypeMismatch behaves like a normal exception."""
    kind = str
    expected_kind = dict
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # It should be an instance of Exception and its base classes
    assert isinstance(exc, Exception)
    assert isinstance(exc, LiteralSortTypeMismatch)
    # Raising and catching should work as expected
    with pytest.raises(LiteralSortTypeMismatch) as cm:
        raise exc
    assert cm.value is exc

def test_literal_sort_type_mismatch_with_non_type_arguments():
    """Test that passing non-type objects still creates the exception
    but the message reflects their actual types."""
    kind = 42          # int instance, not a type
    expected_kind = "string"  # str instance, not a type
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # The message should use the type names of the provided objects
    assert "int" in str(exc)          # type of 42
    assert "str" in str(exc)          # type of "string"
    # Attributes should store the original objects
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind
