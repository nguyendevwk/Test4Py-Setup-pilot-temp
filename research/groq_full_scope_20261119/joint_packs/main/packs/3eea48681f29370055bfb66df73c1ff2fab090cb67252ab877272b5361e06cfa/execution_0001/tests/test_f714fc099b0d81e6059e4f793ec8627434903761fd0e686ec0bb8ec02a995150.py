import pytest
from isort.exceptions import MissingSection, ISortError

def test_missing_section_message_contains_import_and_section():
    """The error message should mention both the import module and the missing section."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    assert "my.module" in str(exc)
    assert "CUSTOM" in str(exc)
    # Ensure the message contains the expected guidance link
    assert "https://isort.readthedocs.io" in str(exc)

def test_missing_section_inherits_from_isort_error():
    """MissingSection must be a subclass of ISortError."""
    exc = MissingSection(import_module="foo", section="BAR")
    assert isinstance(exc, ISortError)
    # ISortError should be a subclass of Exception
    assert isinstance(exc, Exception)

def test_missing_section_with_empty_strings():
    """Even with empty strings, the exception should be constructed without raising."""
    exc = MissingSection(import_module="", section="")
    # The message should still be a string and not empty
    assert isinstance(str(exc), str)
    assert len(str(exc)) > 0
    # It should not contain the literal empty string placeholders
    assert "import" in str(exc) and "section" in str(exc)
