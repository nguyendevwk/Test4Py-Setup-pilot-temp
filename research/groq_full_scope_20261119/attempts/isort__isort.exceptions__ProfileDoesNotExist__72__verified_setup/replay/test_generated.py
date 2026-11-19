import pytest
from isort.exceptions import ProfileDoesNotExist
from isort.profiles import profiles

def test_profile_does_not_exist_message_and_attribute():
    """Instantiating with a missing profile should set the profile attribute
    and produce a message that lists all available profiles."""
    missing_profile = "nonexistent"
    exc = ProfileDoesNotExist(missing_profile)
    # The profile attribute should be stored correctly
    assert exc.profile == missing_profile
    # The message should mention the missing profile
    assert missing_profile in str(exc)
    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)

def test_profile_does_not_exist_with_empty_string():
    """An empty string is also an invalid profile and should be handled."""
    exc = ProfileDoesNotExist("")
    # The profile attribute should be the empty string
    assert exc.profile == ""
    # The message should still reference the empty string
    assert "Specified profile of " in str(exc)
    assert "does not exist" in str(exc)

def test_profile_does_not_exist_with_numeric_profile():
    """Numeric profiles are not valid and should trigger the same error."""
    numeric_profile = "123"
    exc = ProfileDoesNotExist(numeric_profile)
    # The profile attribute should be the numeric string
    assert exc.profile == numeric_profile
    # The message should contain the numeric profile
    assert numeric_profile in str(exc)
