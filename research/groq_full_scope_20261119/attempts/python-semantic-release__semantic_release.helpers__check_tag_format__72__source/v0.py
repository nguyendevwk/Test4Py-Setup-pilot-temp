import pytest
from semantic_release.helpers import check_tag_format

def test_check_tag_format_valid():
    # A format string that includes the required 'version' key should pass silently
    check_tag_format("release-{version}")
    # The function should not raise any exception for a valid format
    # No assertion needed beyond absence of exception

def test_check_tag_format_missing_version():
    # A format string without the 'version' key should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        check_tag_format("release-{rev}")
    # Verify the error message contains the problematic format string
    assert "release-{rev}" in str(excinfo.value)
    # Ensure the message explicitly mentions the missing 'version' key
    assert "must use 'version'" in str(excinfo.value)

def test_check_tag_format_with_additional_keys():
    # The format string may contain other keys; only 'version' is mandatory
    check_tag_format("v{major}.{minor}.{patch}-{version}")
    # No exception should be raised
    # The presence of other keys does not affect validation
