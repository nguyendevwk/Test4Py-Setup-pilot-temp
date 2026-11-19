import pytest
from semantic_release.helpers import check_tag_format

def test_check_tag_format_valid():
    """Valid tag format containing the required 'version' key passes silently."""
    # A simple format string that includes the 'version' placeholder.
    tag_fmt = "release-{version}"
    # No exception should be raised for a valid format.
    check_tag_format(tag_fmt)

def test_check_tag_format_missing_version():
    """Tag format without the 'version' key raises ValueError."""
    # Format string missing the required placeholder.
    tag_fmt = "release-{rev}"
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(tag_fmt)
    # Ensure the error message clearly indicates the missing key.
    assert "must use 'version'" in str(excinfo.value)

def test_check_tag_format_empty_string():
    """An empty string is considered invalid and raises ValueError."""
    tag_fmt = ""
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(tag_fmt)
    # The error message should mention the invalid format.
    assert "Invalid tag_format" in str(excinfo.value)
