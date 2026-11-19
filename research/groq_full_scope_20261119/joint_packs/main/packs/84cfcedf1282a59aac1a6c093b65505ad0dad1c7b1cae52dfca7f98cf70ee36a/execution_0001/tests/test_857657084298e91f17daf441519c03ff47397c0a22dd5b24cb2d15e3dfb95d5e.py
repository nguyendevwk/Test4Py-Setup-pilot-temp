import pytest
from isort.exceptions import AssignmentsFormatMismatch

def test_assignments_format_mismatch_message_contains_code(tmp_path):
    # Create a sample code snippet that would trigger the error
    sample_code = "x = 1\ny = 2\nz = 3"
    exc = AssignmentsFormatMismatch(sample_code)
    # The exception message should include the original code
    assert sample_code in str(exc)
    # It should also contain the expected format description
    assert "{variable_name} = {value}" in str(exc)
    # The code attribute should be set correctly
    assert exc.code == sample_code

def test_assignments_format_mismatch_empty_code():
    # Test with an empty string to ensure the exception still behaves correctly
    empty_code = ""
    exc = AssignmentsFormatMismatch(empty_code)
    # The message should still contain the empty code representation
    assert "isort was told to sort a section of assignments" in str(exc)
    assert empty_code in str(exc)
    # The code attribute should be an empty string
    assert exc.code == ""

def test_assignments_format_mismatch_multiline_error():
    # Provide a multiline assignment that violates the single-line rule
    bad_code = "a = 1\nb =\n    2\nc = 3"
    exc = AssignmentsFormatMismatch(bad_code)
    # The message should include the problematic code block
    assert bad_code in str(exc)
    # The message should still mention the expected format
    assert "Does not match isort's strict single line formatting requirement" in str(exc)
    # Ensure the code attribute retains the original multiline string
    assert exc.code == bad_code
