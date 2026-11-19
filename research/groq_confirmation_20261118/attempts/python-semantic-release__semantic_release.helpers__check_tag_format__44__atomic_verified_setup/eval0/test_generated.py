import pytest
from semantic_release.helpers import check_tag_format

def test_check_tag_format_valid():
    """A tag format containing the required 'version' key should pass silently."""
    # A simple valid format
    check_tag_format("release-{version}")
    # More complex format with other placeholders
    check_tag_format("{env}-{version}-{build}")
    # Format with escaped braces
    check_tag_format("v{{{version}}}")

def test_check_tag_format_missing_version():
    """A tag format that does not contain the 'version' key should raise ValueError."""
    with pytest.raises(ValueError, match=r"must use 'version'"):
        check_tag_format("release-{rev}")
    with pytest.raises(ValueError, match=r"must use 'version'"):
        check_tag_format("v{env}-{build}")

def test_check_tag_format_edge_cases():
    """Edge cases: empty string, only braces, and nested braces should raise ValueError."""
    with pytest.raises(ValueError, match=r"must use 'version'"):
        check_tag_format("")
    with pytest.raises(ValueError, match=r"must use 'version'"):
        check_tag_format("{}")
    with pytest.raises(ValueError, match=r"must use 'version'"):
        check_tag_format("{version}{version}")  # still valid
    # The following is valid because it contains 'version'
    check_tag_format("{version}{env}")
