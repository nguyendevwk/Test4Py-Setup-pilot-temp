import pytest
from semantic_release.helpers import check_tag_format


def test_check_tag_format_valid():
    """A tag format containing the required 'version' key should pass without error."""
    # The format string includes 'version' and an additional placeholder.
    tag_format = "release-{version}-{build}"
    # No exception should be raised for a valid format.
    check_tag_format(tag_format)


def test_check_tag_format_missing_version():
    """A tag format missing the 'version' key should raise a ValueError."""
    # The format string lacks the required 'version' placeholder.
    tag_format = "release-{build}"
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(tag_format)
    # Verify the error message mentions the missing key.
    assert "must use 'version' as a format key" in str(excinfo.value)


def test_check_tag_format_only_version():
    """A tag format that contains only the 'version' key should still be valid."""
    tag_format = "{version}"
    # No exception should be raised for a minimal valid format.
    check_tag_format(tag_format)
