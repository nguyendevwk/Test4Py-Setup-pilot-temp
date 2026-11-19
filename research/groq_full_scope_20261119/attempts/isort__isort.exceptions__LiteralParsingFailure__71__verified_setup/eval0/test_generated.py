import pytest
from isort.exceptions import LiteralParsingFailure, ISortError


def test_literal_parsing_failure_with_exception_instance():
    """LiteralParsingFailure should store the original exception instance."""
    original_exc = ValueError("invalid literal")
    code = "foo = 'bar'"
    failure = LiteralParsingFailure(code, original_exc)

    # The instance should be an ISortError and a subclass of Exception
    assert isinstance(failure, ISortError)
    assert isinstance(failure, Exception)

    # The original_error attribute should reference the same instance
    assert failure.original_error is original_exc

    # The message should include the code and the original exception message
    msg = str(failure)
    assert code in msg
    assert "invalid literal" in msg


def test_literal_parsing_failure_with_exception_type():
    """LiteralParsingFailure should accept an exception type as original_error."""
    code = "x = [1, 2, 3]"
    failure = LiteralParsingFailure(code, SyntaxError)

    # The original_error attribute should be the type itself
    assert failure.original_error is SyntaxError

    # The message should mention the exception type name
    msg = str(failure)
    assert "SyntaxError" in msg
    assert code in msg


def test_literal_parsing_failure_str_and_repr():
    """The string representation should be deterministic and match the message."""
    original_exc = RuntimeError("runtime failure")
    code = "y = {'a': 1}"
    failure = LiteralParsingFailure(code, original_exc)

    # str(failure) should equal the message passed to Exception
    expected_msg = (
        f"isort failed to parse the given literal {code}. "
        "It's important to note that isort literal sorting only supports simple literals "
        "parsable by ast.literal_eval which gave the exception of "
        f"{original_exc}."
    )
    assert str(failure) == expected_msg

    # repr should include the class name and the message
    assert repr(failure).startswith("LiteralParsingFailure(")
    assert expected_msg in repr(failure)
