import pytest
from isort.exceptions import AssignmentsFormatMismatch

def test_assignments_format_mismatch_initialization():
    """The exception should store the provided code and format the message correctly."""
    sample_code = "x = 1\ny = 2"
    exc = AssignmentsFormatMismatch(sample_code)
    # The stored code should match the input
    assert exc.code == sample_code
    # The message should contain the code block
    assert sample_code in str(exc)
    # The message should include the expected format hint
    assert "{variable_name} = {value}" in str(exc)

def test_assignments_format_mismatch_message_contains_newlines():
    """The exception message should preserve newlines from the code argument."""
    code_with_newlines = "a = 10\nb = 20\nc = 30"
    exc = AssignmentsFormatMismatch(code_with_newlines)
    # The message should contain the exact newline structure
    assert "\na = 10\nb = 20\nc = 30\n" in str(exc)

def test_assignments_format_mismatch_inherits_from_exception():
    """The exception should be an instance of Exception and ISortError."""
    exc = AssignmentsFormatMismatch("invalid code")
    # It should be an Exception
    assert isinstance(exc, Exception)
    # It should be an ISortError (imported from isort.exceptions)
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)
