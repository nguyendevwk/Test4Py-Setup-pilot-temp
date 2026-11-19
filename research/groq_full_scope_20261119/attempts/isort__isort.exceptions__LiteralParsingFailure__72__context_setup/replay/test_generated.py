import pytest
from isort.exceptions import LiteralParsingFailure, ISortError


def test_literal_parsing_failure_message_and_attributes():
    """Verify that the exception message contains the provided code and original error."""
    code = "invalid_literal"
    original_error = ValueError("bad literal")
    exc = LiteralParsingFailure(code, original_error)

    # The message should mention the code and the original error message
    assert code in str(exc)
    assert "bad literal" in str(exc)

    # The attributes should be stored correctly
    assert exc.code == code
    assert exc.original_error is original_error


def test_literal_parsing_failure_with_error_type():
    """Ensure that passing an exception type works and is reflected in the message."""
    code = "another_bad_literal"
    original_error = SyntaxError
    exc = LiteralParsingFailure(code, original_error)

    # The message should include the name of the exception type
    assert "SyntaxError" in str(exc)

    # The original_error attribute should be the type itself
    assert exc.original_error is SyntaxError


def test_literal_parsing_failure_inherits_from_isort_error():
    """Check that the exception is a subclass of ISortError and can be caught as such."""
    code = "x"
    original_error = RuntimeError("runtime issue")
    exc = LiteralParsingFailure(code, original_error)

    # It should be an instance of both LiteralParsingFailure and ISortError
    assert isinstance(exc, LiteralParsingFailure)
    assert isinstance(exc, ISortError)

    # It should be catchable via the base class
    try:
        raise exc
    except ISortError as e:
        assert e is exc
