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
    exc = MissingSection("x", "y")
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_raising_missing_section_is_caught_by_pytest():
    """Raising MissingSection should be caught by pytest.raises and provide the correct message."""
    with pytest.raises(MissingSection) as excinfo:
        raise MissingSection("foo.bar", "SPECIAL")
    assert "foo.bar" in str(excinfo.value)
    assert "SPECIAL" in str(excinfo.value)
