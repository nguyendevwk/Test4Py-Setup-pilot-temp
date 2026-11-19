import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details(tmp_path):
    """The exception message should include the import module and section names."""
    exc = MissingSection(import_module="my.module", section="CUSTOM")
    assert "my.module" in str(exc)
    assert "CUSTOM" in str(exc)
    # The message should start with a specific prefix
    assert str(exc).startswith("Found my.module import while parsing, but CUSTOM was not included")


def test_missing_section_inherits_isort_error():
    """MissingSection must be a subclass of ISortError."""
    exc = MissingSection(import_module="x", section="y")
    assert isinstance(exc, ISortError)
    # Ensure that the base Exception message is preserved
    assert isinstance(exc, Exception)


def test_missing_section_with_empty_strings(tmp_path):
    """Creating the exception with empty strings should still produce a valid message."""
    exc = MissingSection(import_module="", section="")
    # The message should not be empty and should reference the empty values
    assert "Found  import while parsing, but  was not included" in str(exc)
    # The exception should still be usable in a with statement
    with pytest.raises(MissingSection) as cm:
        raise exc
    assert cm.value is exc
