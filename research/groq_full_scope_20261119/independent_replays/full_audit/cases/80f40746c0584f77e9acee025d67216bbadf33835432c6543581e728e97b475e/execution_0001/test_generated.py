import pytest
from isort.exceptions import LiteralSortTypeMismatch

def test_literal_sort_type_mismatch_message_and_attributes():
    # Create an instance with mismatched types
    exc = LiteralSortTypeMismatch(int, list)
    # The message should include both the provided and expected types
    assert "type <class 'int'>" in str(exc)
    assert "type <class 'list'>" in str(exc)
    # The attributes should be set correctly
    assert exc.kind is int
    assert exc.expected_kind is list

def test_literal_sort_type_mismatch_str_representation():
    # The string representation should be exactly the message passed to the base class
    exc = LiteralSortTypeMismatch(str, dict)
    expected_msg = (
        "isort was told to sort a literal of type <class 'dict'> but was given "
        "a literal of type <class 'str'>."
    )
    assert str(exc) == expected_msg

def test_literal_sort_type_mismatch_inherits_from_ISortError():
    # Ensure the exception is an instance of the base ISortError class
    exc = LiteralSortTypeMismatch(tuple, set)
    # ISortError is defined in the same package; we can import it directly
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)
