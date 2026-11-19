import pytest
from isort.exceptions import ProfileDoesNotExist
from isort.profiles import profiles

def test_profile_does_not_exist_initializes_with_correct_message_and_attribute():
    """Verify that the exception message contains the missing profile
    and the list of available profiles, and that the profile attribute
    is set correctly."""
    missing_profile = "nonexistent_profile"
    exc = ProfileDoesNotExist(missing_profile)

    # The profile attribute should be stored
    assert exc.profile == missing_profile

    # The message should mention the missing profile
    assert missing_profile in str(exc)

    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)

def test_profile_does_not_exist_with_empty_profile_name():
    """Test that an empty string profile still raises the exception
    and includes the empty profile name in the message."""
    missing_profile = ""
    exc = ProfileDoesNotExist(missing_profile)

    # The profile attribute should be the empty string
    assert exc.profile == ""

    # The message should contain the empty profile name (i.e., start with "Specified profile of ")
    assert str(exc).startswith("Specified profile of ")

    # The message should still list all available profiles
    for p in profiles:
        assert p in str(exc)

def test_profile_does_not_exist_with_numeric_profile_name():
    """Test that a numeric string profile name is handled correctly."""
    missing_profile = "12345"
    exc = ProfileDoesNotExist(missing_profile)

    # The profile attribute should be the numeric string
    assert exc.profile == missing_profile

    # The message should contain the numeric profile name
    assert missing_profile in str(exc)

    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)
