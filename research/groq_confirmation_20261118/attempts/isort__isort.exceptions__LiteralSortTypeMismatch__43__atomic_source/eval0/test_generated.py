import pytest
from isort.exceptions import LiteralSortTypeMismatch, ISortError


def test_literal_sort_type_mismatch_initialization_and_message(tmp_path):
    """Verify that the exception stores the provided types and constructs the correct message."""
    kind = list
    expected_kind = dict
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)

    # The stored attributes should match the arguments
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

    # The message should mention both types by name
    expected_msg = (
        f"isort was told to sort a literal of type {expected_kind} but was given "
        f"a literal of type {kind}."
    )
    assert str(exc) == expected_msg


def test_literal_sort_type_mismatch_with_same_type(tmp_path):
    """When the provided kind matches the expected kind, the message still reflects the mismatch."""
    kind = dict
    expected_kind = dict
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # Even though the types are the same, the exception is still raised
    assert isinstance(exc, ISortError)
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

    # The message should correctly reference the type names
    expected_msg = (
        f"isort was told to sort a literal of type {expected_kind} but was given "
        f"a literal of type {kind}."
    )
    assert str(exc) == expected_msg


def test_literal_sort_type_mismatch_inherits_from_base_exception(tmp_path):
    """Ensure that LiteralSortTypeMismatch is a subclass of Exception and can be caught as such."""
    kind = set
    expected_kind = list
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # It should be catchable by a generic Exception handler
    try:
        raise exc
    except Exception as e:
        assert e is exc
        # The caught exception should still be an instance of LiteralSortTypeMismatch
        assert isinstance(e, LiteralSortTypeMismatch)
        # And also an instance of ISortError
        assert isinstance(e, ISortError)
