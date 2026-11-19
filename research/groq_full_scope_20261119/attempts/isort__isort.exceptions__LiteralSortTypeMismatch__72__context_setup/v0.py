import pytest
from isort.exceptions import LiteralSortTypeMismatch, ISortError


def test_literal_sort_type_mismatch_message_and_attributes():
    """Verify that the exception message contains the expected type names
    and that the attributes are set correctly."""
    exc = LiteralSortTypeMismatch(int, list)
    assert isinstance(exc, ISortError)
    assert exc.kind is int
    assert exc.expected_kind is list
    expected_msg = (
        "isort was told to sort a literal of type list but was given "
        "a literal of type int."
    )
    assert str(exc) == expected_msg


def test_literal_sort_type_mismatch_with_custom_types():
    """Test the exception with custom classes to ensure type names are rendered."""
    class CustomKind:  # noqa: D101
        pass

    class ExpectedKind:  # noqa: D101
        pass

    exc = LiteralSortTypeMismatch(CustomKind, ExpectedKind)
    assert exc.kind is CustomKind
    assert exc.expected_kind is ExpectedKind
    assert "CustomKind" in str(exc)
    assert "ExpectedKind" in str(exc)


def test_literal_sort_type_mismatch_is_not_swallowed_by_generic_exception():
    """Ensure that the exception is not caught by a generic Exception handler
    that expects ISortError, but is still a subclass of Exception."""
    exc = LiteralSortTypeMismatch(str, tuple)
    try:
        raise exc
    except ISortError as e:
        # The exception should be caught here because it is a subclass of ISortError
        assert e is exc
    except Exception:
        pytest.fail("LiteralSortTypeMismatch should be caught as ISortError")
