import pytest
from isort.exceptions import LiteralSortTypeMismatch

def test_literal_sort_type_mismatch_message_and_attributes():
    # Arrange: create an exception with mismatched types
    kind = list
    expected_kind = dict
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # Assert: the message contains both type names
    assert "list" in str(exc)
    assert "dict" in str(exc)

    # Assert: the attributes are set correctly
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

def test_literal_sort_type_mismatch_inherits_from_isort_error():
    # Arrange: create an exception
    exc = LiteralSortTypeMismatch(int, str)

    # Assert: it is an instance of the base ISortError class
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)

def test_literal_sort_type_mismatch_with_non_type_arguments():
    # Arrange: pass non-type objects to the constructor
    kind = "not_a_type"
    expected_kind = 42

    # Act & Assert: the constructor should still accept them and store them
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    assert exc.kind == kind
    assert exc.expected_kind == expected_kind
    # The message should reflect the string representations
    assert "not_a_type" in str(exc)
    assert "42" in str(exc)
