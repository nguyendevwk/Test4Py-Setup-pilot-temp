import pytest
from isort.exceptions import AssignmentsFormatMismatch, ISortError


def test_assignments_format_mismatch_initialization():
    """The exception should store the provided code and format the message correctly."""
    sample_code = "x = 1\ny = 2"
    exc = AssignmentsFormatMismatch(sample_code)
    # The message should contain the original code
    assert sample_code in str(exc)
    # The message should mention the expected format
    assert "{variable_name} = {value}" in str(exc)
    # The code attribute should be set to the original string
    assert exc.code == sample_code


def test_assignments_format_mismatch_inherits_isort_error():
    """AssignmentsFormatMismatch must be a subclass of ISortError."""
    exc = AssignmentsFormatMismatch("dummy")
    assert isinstance(exc, ISortError)
    # ISortError is a subclass of Exception
    assert isinstance(exc, Exception)


def test_assignments_format_mismatch_message_consistency():
    """The message should be deterministic and not change across multiple accesses."""
    code = "a = 10\nb = 20"
    exc = AssignmentsFormatMismatch(code)
    first_message = str(exc)
    second_message = str(exc)
    # The message should be the same each time
    assert first_message == second_message
    # The message should not contain any stray formatting placeholders
    assert "{" not in first_message.replace("{variable_name}", "").replace("{value}", "")
