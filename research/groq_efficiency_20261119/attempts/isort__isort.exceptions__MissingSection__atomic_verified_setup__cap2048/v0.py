import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_import_and_section():
    """The error message should include the import module and the missing section."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    msg = str(exc)
    assert "my.module" in msg
    assert "CUSTOM" in msg
    assert "Found my.module import while parsing" in msg
    assert "CUSTOM was not included" in msg


def test_missing_section_inherits_from_isort_error_and_exception():
    """MissingSection should be a subclass of ISortError and Exception."""
    exc = MissingSection(import_module="x", section="y")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_with_empty_strings():
    """Creating the exception with empty strings should still produce a valid message."""
    exc = MissingSection(import_module="", section="")
    msg = str(exc)
    # The message should still contain the placeholders even if empty
    assert "Found  import while parsing" in msg
    assert " was not included" in msg
    # No unexpected exceptions should be raised
    assert isinstance(exc, Exception)
