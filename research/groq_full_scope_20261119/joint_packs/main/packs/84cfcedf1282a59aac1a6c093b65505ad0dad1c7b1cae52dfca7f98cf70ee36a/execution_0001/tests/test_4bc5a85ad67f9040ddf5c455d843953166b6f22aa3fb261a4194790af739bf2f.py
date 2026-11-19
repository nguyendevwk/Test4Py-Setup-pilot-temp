import pytest
from isort.exceptions import AssignmentsFormatMismatch
from isort.exceptions import ISortError

def test_assignments_format_mismatch_inherits_and_has_code(tmp_path):
    """The exception should inherit from ISortError and store the provided code."""
    sample_code = "x = 1\ny = 2"
    exc = AssignmentsFormatMismatch(sample_code)
    # Inheritance check
    assert isinstance(exc, ISortError)
    # Code attribute check
    assert exc.code == sample_code
    # The message should contain the code
    assert sample_code in str(exc)

def test_message_contains_expected_template(tmp_path):
    """The error message should include the expected assignment format template."""
    sample_code = "a=1\nb=2"
    exc = AssignmentsFormatMismatch(sample_code)
    msg = str(exc)
    # The template lines should be present verbatim
    assert "{variable_name} = {value}" in msg
    assert "{variable_name2} = {value2}" in msg
    # The code snippet should be surrounded by blank lines as in the definition
    assert f"\n\n{sample_code}\n\n" in msg

def test_error_message_is_consistent_across_instances(tmp_path):
    """Two instances with the same code should produce identical messages."""
    code = "foo = 'bar'\nbar = 42"
    exc1 = AssignmentsFormatMismatch(code)
    exc2 = AssignmentsFormatMismatch(code)
    assert str(exc1) == str(exc2)
    # Ensure that the message is not empty
    assert len(str(exc1)) > 0
