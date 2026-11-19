import pytest
from isort.exceptions import ProfileDoesNotExist
from isort.profiles import profiles


def test_profile_does_not_exist_message_and_attribute():
    """The exception should contain the profile name and list of available profiles."""
    profile_name = "nonexistent"
    exc = ProfileDoesNotExist(profile_name)
    # The profile attribute should be set correctly
    assert exc.profile == profile_name
    # The message should mention the missing profile
    assert f"Specified profile of {profile_name} does not exist." in str(exc)
    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)


def test_profile_does_not_exist_raises_and_catches():
    """Raising the exception should propagate correctly and be catchable."""
    with pytest.raises(ProfileDoesNotExist) as excinfo:
        raise ProfileDoesNotExist("missing")
    # The caught exception should be the same instance
    assert isinstance(excinfo.value, ProfileDoesNotExist)
    # The message should contain the profile name
    assert "missing" in str(excinfo.value)


def test_profile_does_not_exist_str_representation():
    """The string representation should be deterministic and include all required parts."""
    profile_name = "foo"
    exc = ProfileDoesNotExist(profile_name)
    expected_start = f"Specified profile of {profile_name} does not exist."
    expected_end = f"Available profiles: {','.join(profiles)}."
    message = str(exc)
    assert message.startswith(expected_start)
    assert message.endswith(expected_end)
