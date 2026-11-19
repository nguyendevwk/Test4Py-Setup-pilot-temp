import pytest
from isort.exceptions import LiteralParsingFailure, ISortError


def test_literal_parsing_failure_initialization():
    """Verify that the exception stores the provided code and original error."""
    code = "invalid_literal"
    original_error = ValueError("bad literal")
    exc = LiteralParsingFailure(code, original_error)

    assert isinstance(exc, ISortError)
    assert exc.code == code
    assert exc.original_error is original_error
    assert "invalid_literal" in str(exc)
    assert "ValueError" in str(exc)


def test_literal_parsing_failure_with_empty_code():
    """Ensure that an empty code string is handled correctly."""
    code = ""
    original_error = SyntaxError("empty code")
    exc = LiteralParsingFailure(code, original_error)

    assert exc.code == code
    assert exc.original_error is original_error
    # The message should still contain the empty code representation
    assert "the given literal " in str(exc)
    assert "empty code" in str(exc)


def test_literal_parsing_failure_original_error_type():
    """Test that passing a type of exception works and is reflected in the message."""
    code = "123"
    original_error_type = TypeError
    exc = LiteralParsingFailure(code, original_error_type)

    assert exc.original_error is original_error_type
    assert "TypeError" in str(exc)
    assert "123" in str(exc)
