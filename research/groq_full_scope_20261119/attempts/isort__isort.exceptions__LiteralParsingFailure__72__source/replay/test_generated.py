import pytest
from isort.exceptions import LiteralParsingFailure, ISortError


def test_literal_parsing_failure_message_and_attributes():
    code = "invalid_literal"
    original_error = ValueError("bad literal")
    exc = LiteralParsingFailure(code, original_error)

    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)

    # The message should mention the code and the original error message
    assert code in str(exc)
    assert "bad literal" in str(exc)

    # The attributes should be stored correctly
    assert exc.code == code
    assert exc.original_error is original_error


def test_literal_parsing_failure_with_exception_type():
    code = "another_invalid"
    original_error_type = SyntaxError
    exc = LiteralParsingFailure(code, original_error_type)

    # The message should include the exception type name
    assert "SyntaxError" in str(exc)

    # The original_error attribute should be the exception type itself
    assert exc.original_error is original_error_type


def test_literal_parsing_failure_message_format():
    code = "x"
    original_error = RuntimeError("oops")
    exc = LiteralParsingFailure(code, original_error)

    # The message should start with a fixed prefix
    expected_prefix = "isort failed to parse the given literal"
    assert str(exc).startswith(expected_prefix)

    # The message should end with the original error string
    assert str(exc).endswith(f"gave the exception of {original_error}.")
