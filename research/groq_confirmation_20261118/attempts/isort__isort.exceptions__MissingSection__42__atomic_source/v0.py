import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_contains_details(tmp_path):
    """Ensure the exception message includes the import module and section."""
    exc = MissingSection(import_module="my_module", section="CUSTOM")
    msg = str(exc)
    assert "my_module" in msg
    assert "CUSTOM" in msg
    assert "Found my_module import while parsing" in msg
    assert "CUSTOM was not included" in msg
    assert "sections setting of your config" in msg
    assert "See https://isort.readthedocs.io" in msg


def test_missing_section_inherits_isort_error():
    """Verify that MissingSection is a subclass of ISortError."""
    exc = MissingSection(import_module="foo", section="BAR")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_raises_with_invalid_section(tmp_path):
    """Confirm that creating the exception with an empty section still raises an error."""
    with pytest.raises(MissingSection) as excinfo:
        MissingSection(import_module="foo", section="")
    assert "Found foo import while parsing" in str(excinfo.value)
    assert "was not included" in str(excinfo.value)
