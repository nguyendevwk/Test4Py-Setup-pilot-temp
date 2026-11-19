import pytest
from semantic_release.helpers import check_tag_format

def test_check_tag_format_valid():
    # A tag format that includes the required 'version' key should pass without error
    valid_format = "release-{version}"
    # No exception should be raised
    check_tag_format(valid_format)

def test_check_tag_format_missing_version():
    # A tag format that does not include the 'version' key should raise ValueError
    invalid_format = "release-{rev}"
    with pytest.raises(ValueError) as excinfo:
        check_tag_format(invalid_format)
    # The error message should explicitly mention the missing 'version' key
    assert "must use 'version' as a format key" in str(excinfo.value)

def test_check_tag_format_other_keys_allowed():
    # The format may contain other keys; only 'version' is mandatory
    mixed_format = "v{major}.{minor}.{patch}-{version}"
    # Should not raise an exception
    check_tag_format(mixed_format)
