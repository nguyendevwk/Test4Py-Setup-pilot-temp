import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message_and_inheritance(tmp_path):
    """Verify that MissingSection produces the correct message and inherits from ISortError."""
    import_module = "my_module"
    section = "CUSTOM"
    exc = MissingSection(import_module, section)
    # The exception should be an instance of ISortError
    assert isinstance(exc, ISortError)
    # The message should contain both the import module and the missing section
    msg = str(exc)
    assert import_module in msg
    assert section in msg
    # The message should include the guidance URL
    assert "https://isort.readthedocs.io" in msg


def test_missing_section_str_representation(tmp_path):
    """Ensure that str(MissingSection(...)) returns the expected formatted string."""
    exc = MissingSection("foo.bar", "FOO")
    expected_start = "Found foo.bar import while parsing, but FOO was not included"
    assert str(exc).startswith(expected_start)


def test_missing_section_error_raised_in_context(tmp_path):
    """Confirm that raising MissingSection propagates correctly in a try/except block."""
    with pytest.raises(MissingSection) as excinfo:
        raise MissingSection("x.y", "XYZ")
    # The exception message should match the one constructed in the raise
    assert "x.y" in str(excinfo.value)
    assert "XYZ" in str(excinfo.value)
