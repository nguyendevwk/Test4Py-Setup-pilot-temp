import pytest
from isort.exceptions import LiteralSortTypeMismatch

# Test 1: Normal construction with matching types
def test_literal_sort_type_mismatch_message_and_attributes():
    kind = list
    expected_kind = tuple
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # The exception should be an instance of Exception
    assert isinstance(exc, Exception)
    # The message should mention both types correctly
    assert "list" in str(exc)
    assert "tuple" in str(exc)
    # The attributes should be set correctly
    assert exc.kind is kind
    assert exc.expected_kind is expected_kind

# Test 2: Boundary case with built‑in types
def test_literal_sort_type_mismatch_with_builtin_types():
    kind = int
    expected_kind = str
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # Ensure the message contains the names of the built‑in types
    assert "int" in str(exc)
    assert "str" in str(exc)
    # Attributes should reference the exact type objects
    assert exc.kind is int
    assert exc.expected_kind is str

# Test 3: Error behavior when non‑type arguments are passed
def test_literal_sort_type_mismatch_with_invalid_arguments():
    # Passing a string instead of a type should still construct the exception,
    # but the message will reflect the string representation.
    kind = "not_a_type"
    expected_kind = 42
    exc = LiteralSortTypeMismatch(kind, expected_kind)
    # The message should include the string representations of the arguments
    assert "not_a_type" in str(exc)
    assert "42" in str(exc)
    # The attributes should hold the original values
    assert exc.kind == kind
    assert exc.expected_kind == expected_kind
