import pytest
from isort.exceptions import MissingSection

def test_missing_section_message_contains_details():
    """The error message should include the import module and the missing section."""
    exc = MissingSection("my_module", "CUSTOM")
    assert "my_module" in str(exc)
    assert "CUSTOM" in str(exc)
    assert "Found my_module import while parsing" in str(exc)
    assert "CUSTOM was not included" in str(exc)

def test_missing_section_inherits_from_exception():
    """MissingSection should be a subclass of Exception."""
    exc = MissingSection("foo", "BAR")
    assert isinstance(exc, Exception)
    # Ensure it is not an unrelated type
    assert not isinstance(exc, ValueError)

def test_missing_section_can_be_raised_and_caught():
    """Raising MissingSection should propagate correctly and be caught by pytest.raises."""
    with pytest.raises(MissingSection) as excinfo:
        raise MissingSection("spam", "EGGS")
    assert excinfo.value.import_module == "spam"  # attribute not defined, but check message
    assert "spam" in str(excinfo.value)
    assert "EGGS" in str(excinfo.value)
