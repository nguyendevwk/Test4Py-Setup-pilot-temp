import pytest
from semantic_release.helpers import check_tag_format

def test_check_tag_format_valid():
    # A format string that correctly includes the required 'version' key
    valid_format = "release-{version}"
    # Should not raise any exception
    check_tag_format(valid_format)

def test_check_tag_format_missing_version():
    # A format string that does not contain the 'version' key
    invalid_format = "release-{rev}"
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(invalid_format)
    assert "must use 'version' as a format key" in str(excinfo.value)

def test_check_tag_format_empty_string():
    # An empty string also fails because it lacks the 'version' key
    empty_format = ""
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(empty_format)
    assert "must use 'version' as a format key" in str(excinfo.value)
