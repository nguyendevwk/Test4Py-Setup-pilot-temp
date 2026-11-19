import pytest
from isort.exceptions import LiteralParsingFailure
import ast

def test_literal_parsing_failure_message_contains_code_and_error():
    code = "invalid_literal"
    original_error = ValueError("bad literal")
    exc = LiteralParsingFailure(code, original_error)
    assert code in str(exc)
    assert "bad literal" in str(exc)
    assert isinstance(exc.original_error, ValueError)
    assert exc.code == code

def test_literal_parsing_failure_with_error_type():
    code = "another_invalid"
    original_error_type = SyntaxError
    exc = LiteralParsingFailure(code, original_error_type)
    assert code in str(exc)
    assert "SyntaxError" in str(exc)
    assert exc.original_error is original_error_type
    assert exc.code == code

def test_literal_parsing_failure_message_format():
    code = "123"
    original_error = ast.literal_eval("not_a_literal")
    exc = LiteralParsingFailure(code, original_error)
    msg = str(exc)
    expected_start = "isort failed to parse the given literal 123."
    assert msg.startswith(expected_start)
    assert "ast.literal_eval" in msg
    assert "SyntaxError" in msg or "ValueError" in msg
