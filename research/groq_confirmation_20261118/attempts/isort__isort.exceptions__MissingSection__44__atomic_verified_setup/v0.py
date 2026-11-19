import pytest
from isort.exceptions import MissingSection
from isort.exceptions import ISortError

def test_missing_section_message_contains_details():
    """The error message should include the import module and section names."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    expected_substring = "Found my.module import while parsing, but CUSTOM was not included"
    assert expected_substring in str(exc), f"Message missing expected text: {str(exc)}"

def test_missing_section_inherits_from_isort_error_and_exception():
    """MissingSection should be a subclass of both ISortError and Exception."""
    exc = MissingSection(import_module="x", section="y")
    assert isinstance(exc, ISortError), "MissingSection is not an ISortError"
    assert isinstance(exc, Exception), "MissingSection is not an Exception"

def test_missing_section_boundary_empty_strings():
    """Creating MissingSection with empty strings should still produce a valid message."""
    exc = MissingSection(import_module="", section="")
    # The message should still contain the placeholders even if empty
    assert "Found  import while parsing, but  was not included" in str(exc)
