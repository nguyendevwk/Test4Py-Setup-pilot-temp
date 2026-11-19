import pytest
from isort.exceptions import MissingSection, ISortError


def test_missing_section_message(tmp_path):
    """Verify that MissingSection produces the expected error message."""
    module_name = "my_module"
    section_name = "CUSTOM"
    exc = MissingSection(module_name, section_name)
    expected_start = f"Found {module_name} import while parsing, but {section_name} was not included"
    assert str(exc).startswith(expected_start)
    assert "Please add it before continuing" in str(exc)
    assert "https://isort.readthedocs.io" in str(exc)


def test_missing_section_inherits_isort_error():
    """Ensure MissingSection is a subclass of ISortError."""
    module_name = "another_module"
    section_name = "ANOTHER"
    exc = MissingSection(module_name, section_name)
    assert isinstance(exc, ISortError)
    assert isinstance(exc, Exception)


def test_missing_section_with_empty_section_name(tmp_path):
    """Test behavior when an empty section name is provided."""
    module_name = "empty_section_module"
    section_name = ""
    exc = MissingSection(module_name, section_name)
    # The message should still contain the module name and indicate missing section
    assert f"Found {module_name} import while parsing" in str(exc)
    assert "but  was not included" in str(exc)  # empty section placeholder
    assert "Please add it before continuing" in str(exc)
