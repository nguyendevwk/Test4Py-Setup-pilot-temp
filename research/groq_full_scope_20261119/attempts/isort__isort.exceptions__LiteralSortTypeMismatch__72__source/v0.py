import pytest
from isort.exceptions import LiteralSortTypeMismatch

def test_literal_sort_type_mismatch_initialization():
    """Test that the exception stores the provided kinds and constructs the message correctly."""
    kind = list
    expected_kind = tuple
    exc = LiteralSortTypeMismatch(kind, expected_kind)

    # The message should mention both kinds by name
    assert "list" in str(exc)
    assert "tuple" in str(exc)

    # The attributes should be set to the exact objects passed
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

def test_literal_sort_type_mismatch_message_format():
    """Test that the message format matches the specification."""
    kind = dict
    expected_kind = set
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    expected_msg = (
        "isort was told to sort a literal of type set but was given "
        "a literal of type dict."
    )
    # The message should be exactly as expected
    assert str(exc) == expected_msg

def test_literal_sort_type_mismatch_inherits_from_isort_error():
    """Ensure that LiteralSortTypeMismatch is a subclass of ISortError."""
    from isort.exceptions import ISortError
    kind = int
    expected_kind = float
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)
