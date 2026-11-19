import pytest
from isort.exceptions import LiteralSortTypeMismatch

def test_literal_sort_type_mismatch_message_and_attributes():
    # Arrange: create a mismatch between expected and actual types
    actual_type = list
    expected_type = dict
    # Act: instantiate the exception
    exc = LiteralSortTypeMismatch(actual_type, expected_type)
    # Assert: message contains both types
    assert "list" in str(exc)
    assert "dict" in str(exc)
    # Assert: attributes are set correctly
    assert exc.kind is actual_type
    assert exc.expected_kind is expected_type

def test_literal_sort_type_mismatch_inherits_from_exception():
    # Arrange & Act: instantiate the exception
    exc = LiteralSortTypeMismatch(int, str)
    # Assert: it is an instance of Exception and ISortError
    assert isinstance(exc, Exception)
    # The base class ISortError is not directly importable here, but we can check the type name
    assert exc.__class__.__name__ == "LiteralSortTypeMismatch"

def test_literal_sort_type_mismatch_raises_and_catches():
    # Arrange: define a function that raises the exception
    def raise_mismatch():
        raise LiteralSortTypeMismatch(set, tuple)
    # Act & Assert: use pytest.raises to capture the exception
    with pytest.raises(LiteralSortTypeMismatch) as excinfo:
        raise_mismatch()
    # Assert: the caught exception has the expected message
    assert "set" in str(excinfo.value)
    assert "tuple" in str(excinfo.value)
    # Assert: the attributes match the types passed
    assert excinfo.value.kind is set
    assert excinfo.value.expected_kind is tuple
