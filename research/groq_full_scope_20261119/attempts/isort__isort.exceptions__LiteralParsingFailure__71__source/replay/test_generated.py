import pytest
from isort.exceptions import LiteralParsingFailure, ISortError


def test_literal_parsing_failure_message_and_attributes():
    """Verify that the exception message contains the provided code and original error
    and that the attributes are stored correctly."""
    code = "invalid_literal"
    original_error = ValueError("bad literal")
    exc = LiteralParsingFailure(code, original_error)

    # The message should mention the code and the original error message
    assert code in str(exc)
    assert "bad literal" in str(exc)

    # The attributes should be set correctly
    assert exc.code == code
    assert exc.original_error is original_error


def test_literal_parsing_failure_with_error_type():
    """Passing an exception type instead of an instance should still work."""
    code = "another_invalid"
    original_error_type = SyntaxError
    exc = LiteralParsingFailure(code, original_error_type)

    # The message should include the name of the exception type
    assert "SyntaxError" in str(exc)

    # The original_error attribute should be the type itself
    assert exc.original_error is original_error_type


def test_literal_parsing_failure_is_subclass_of_isort_error():
    """Ensure that LiteralParsingFailure is a subclass of ISortError."""
    exc = LiteralParsingFailure("code", RuntimeError("oops"))
    assert isinstance(exc, ISortError)
