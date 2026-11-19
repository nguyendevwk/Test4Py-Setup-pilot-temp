import pytest
from isort.exceptions import LiteralSortTypeMismatch

def test_message_and_attributes():
    """Creating the exception with mismatched types should store the types and format the message."""
    exc = LiteralSortTypeMismatch(list, dict)
    assert exc.kind is list
    assert exc.expected_kind is dict
    expected_msg = (
        "isort was told to sort a literal of type dict but was given "
        "a literal of type list."
    )
    assert str(exc) == expected_msg

def test_same_type_no_error():
    """If the provided kind matches the expected kind, the exception should still be created but the message reflects equality."""
    exc = LiteralSortTypeMismatch(dict, dict)
    assert exc.kind is dict
    assert exc.expected_kind is dict
    expected_msg = (
        "isort was told to sort a literal of type dict but was given "
        "a literal of type dict."
    )
    assert str(exc) == expected_msg

def test_non_type_argument():
    """Passing a non-type as kind should not raise, but the message will include the actual value."""
    exc = LiteralSortTypeMismatch(42, list)
    assert exc.kind == 42
    assert exc.expected_kind is list
    expected_msg = (
        "isort was told to sort a literal of type list but was given "
        "a literal of type 42."
    )
    assert str(exc) == expected_msg
