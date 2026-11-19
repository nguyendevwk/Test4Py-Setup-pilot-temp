import pytest
from isort.exceptions import AssignmentsFormatMismatch, ISortError

def test_assignments_format_mismatch_inherits_exception():
    """The custom exception should inherit from Exception and ISortError."""
    exc = AssignmentsFormatMismatch("x = 1")
    assert isinstance(exc, Exception)
    assert isinstance(exc, ISortError)
    assert isinstance(exc, AssignmentsFormatMismatch)

def test_assignments_format_mismatch_message_contains_code_and_template():
    """The exception message should include the provided code and the expected format template."""
    code = "foo = 42\nbar = 'baz'"
    exc = AssignmentsFormatMismatch(code)
    # The message should start with the generic explanation
    assert exc.args[0].startswith("isort was told to sort a section of assignments")
    # It should contain the original code block
    assert code in exc.args[0]
    # It should contain the expected format template
    assert "{variable_name} = {value}" in exc.args[0]
    assert "{variable_name2} = {value2}" in exc.args[0]

def test_assignments_format_mismatch_code_attribute_set():
    """The exception should expose the original code via the `code` attribute."""
    code = "a = 1\nb = 2"
    exc = AssignmentsFormatMismatch(code)
    assert exc.code == code
