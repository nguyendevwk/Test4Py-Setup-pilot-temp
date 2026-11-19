import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message():
    """The exception message should contain the import module and section."""
    exc = MissingSection(import_module="foo.bar", section="CUSTOM")
    assert "foo.bar" in str(exc)
    assert "CUSTOM" in str(exc)
    assert "Found foo.bar import while parsing" in str(exc)
    assert "CUSTOM was not included" in str(exc)


def test_missing_section_inheritance():
    """MissingSection should inherit from ISortError."""
    exc = MissingSection(import_module="x", section="y")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_with_empty_strings():
    """Passing empty strings should still produce a valid message."""
    exc = MissingSection(import_module="", section="")
    msg = str(exc)
    assert "Found  import while parsing" in msg
    assert " was not included" in msg
    # Ensure no unexpected exceptions are raised during string formatting
    assert isinstance(msg, str)
