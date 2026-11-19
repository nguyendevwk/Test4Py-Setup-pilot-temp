import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details():
    """The exception message should include the import module and section names."""
    exc = MissingSection(import_module="my_module", section="CUSTOM")
    assert "my_module" in str(exc)
    assert "CUSTOM" in str(exc)
    # The message should start with a clear description
    assert str(exc).startswith("Found my_module import while parsing, but CUSTOM was not included")


def test_missing_section_inherits_from_isort_error():
    """MissingSection must be a subclass of ISortError."""
    exc = MissingSection(import_module="foo", section="bar")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_with_empty_strings():
    """Providing empty strings should still produce a valid exception message."""
    exc = MissingSection(import_module="", section="")
    # The message should not be empty and should contain the placeholders
    assert "Found  import while parsing, but  was not included" in str(exc)
    # Ensure that the exception can be raised and caught normally
    with pytest.raises(MissingSection) as cm:
        raise MissingSection(import_module="", section="")
    assert cm.value is exc
