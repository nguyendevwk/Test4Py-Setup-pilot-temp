import pytest
from isort.exceptions import AssignmentsFormatMismatch, ISortError


def test_assignments_format_mismatch_initialization():
    """The exception should store the provided code and be an instance of ISortError."""
    sample_code = "x = 1\ny = 2"
    exc = AssignmentsFormatMismatch(sample_code)
    # The exception instance should be an ISortError
    assert isinstance(exc, ISortError)
    # The code attribute should be exactly the string passed in
    assert exc.code == sample_code


def test_assignments_format_mismatch_message_contains_code_and_format():
    """The exception message should include the code and the expected format template."""
    sample_code = "foo = 42\nbar = 'baz'"
    exc = AssignmentsFormatMismatch(sample_code)
    msg = str(exc)
    # The message must contain the original code block
    assert sample_code in msg
    # The message must contain the expected format description
    assert "{variable_name} = {value}" in msg
    assert "{variable_name2} = {value2}" in msg
    # The message should not contain the raw code twice
    assert msg.count(sample_code) == 1


def test_assignments_format_mismatch_raises_with_invalid_input():
    """Creating the exception with non-string input should raise a TypeError."""
    with pytest.raises(TypeError):
        # Passing an integer should trigger a TypeError because __init__ expects a str
        AssignmentsFormatMismatch(123)
