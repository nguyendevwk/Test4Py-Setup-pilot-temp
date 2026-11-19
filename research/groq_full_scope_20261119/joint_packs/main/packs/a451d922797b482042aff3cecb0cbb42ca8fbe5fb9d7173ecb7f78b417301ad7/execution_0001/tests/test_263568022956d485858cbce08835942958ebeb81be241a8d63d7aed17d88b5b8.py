import pytest
from isort.exceptions import ProfileDoesNotExist
from isort.profiles import profiles


def test_profile_does_not_exist_initializes_with_correct_message_and_attribute():
    """ProfileDoesNotExist should store the profile and construct the error message."""
    missing_profile = "nonexistent_profile"
    exc = ProfileDoesNotExist(missing_profile)

    # The profile attribute should be set correctly
    assert exc.profile == missing_profile

    # The message should mention the missing profile
    assert missing_profile in str(exc)

    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)


def test_profile_does_not_exist_message_is_consistent_across_instances():
    """Two instances with the same missing profile should produce identical messages."""
    profile_name = "foo"
    exc1 = ProfileDoesNotExist(profile_name)
    exc2 = ProfileDoesNotExist(profile_name)

    assert str(exc1) == str(exc2)
    assert exc1.profile == exc2.profile


def test_profile_does_not_exist_raises_when_accessed_as_exception():
    """The exception should be catchable and its message should be usable."""
    missing = "bar"
    with pytest.raises(ProfileDoesNotExist) as excinfo:
        raise ProfileDoesNotExist(missing)

    # The caught exception should be the same type
    assert isinstance(excinfo.value, ProfileDoesNotExist)

    # The message should contain the missing profile name
    assert missing in str(excinfo.value)

    # The message should include the list of available profiles
    for p in profiles:
        assert p in str(excinfo.value)
