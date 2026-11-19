import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details(tmp_path):
    """The exception message should include the import module and section names."""
    exc = MissingSection("my.module", "CUSTOM")
    assert "my.module" in str(exc)
    assert "CUSTOM" in str(exc)
    # The message should start with a clear prefix
    assert str(exc).startswith("Found my.module import while parsing, but CUSTOM was not included")


def test_missing_section_inherits_from_isort_error():
    """MissingSection must be a subclass of ISortError and Exception."""
    exc = MissingSection("foo", "BAR")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_accepts_non_string_inputs():
    """Passing non-string arguments should still produce a valid message."""
    exc = MissingSection(123, None)
    # The string representation should convert the arguments to strings
    assert "123" in str(exc)
    assert "None" in str(exc)
