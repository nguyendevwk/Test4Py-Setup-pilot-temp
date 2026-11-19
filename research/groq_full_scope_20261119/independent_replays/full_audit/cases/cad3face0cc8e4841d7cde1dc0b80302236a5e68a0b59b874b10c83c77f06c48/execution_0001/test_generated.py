import pytest
from isort.exceptions import MissingSection


def test_missing_section_message_contains_import_and_section():
    """The error message should include the import module and the missing section."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    assert "my.module" in str(exc)
    assert "CUSTOM" in str(exc)
    # The message should contain the guidance link
    assert "https://isort.readthedocs.io" in str(exc)


def test_missing_section_with_empty_strings():
    """Passing empty strings should still produce a valid error message."""
    exc = MissingSection(import_module="", section="")
    msg = str(exc)
    # Even with empty values, the message should not be empty and should still contain the link
    assert msg, "Message should not be empty"
    assert "https://isort.readthedocs.io" in msg
    # The placeholders should be present but empty
    assert "Found  import while parsing" in msg
    assert "was not included in the `sections` setting" in msg


def test_missing_section_is_exception_and_subclass_of_ISortError():
    """MissingSection should be an exception and subclass of ISortError."""
    exc = MissingSection(import_module="foo", section="bar")
    # It should be an instance of Exception
    assert isinstance(exc, Exception)
    # It should also be an instance of the base ISortError class
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError)
