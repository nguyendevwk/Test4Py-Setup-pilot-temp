import pytest
from isort.exceptions import ProfileDoesNotExist, ISortError
from isort.profiles import profiles


def test_profile_does_not_exist_message(tmp_path):
    """The exception message should mention the missing profile and list available profiles."""
    missing_profile = "nonexistent"
    exc = ProfileDoesNotExist(missing_profile)
    # The message should contain the missing profile name
    assert missing_profile in str(exc)
    # The message should list all available profiles
    for p in profiles:
        assert p in str(exc)
    # The message should start with the expected prefix
    assert str(exc).startswith(f"Specified profile of {missing_profile} does not exist.")


def test_profile_attribute_set(tmp_path):
    """The exception should expose the missing profile via the `profile` attribute."""
    missing_profile = "ghost"
    exc = ProfileDoesNotExist(missing_profile)
    assert exc.profile == missing_profile


def test_isort_error_inheritance(tmp_path):
    """ProfileDoesNotExist should be a subclass of ISortError."""
    missing_profile = "phantom"
    exc = ProfileDoesNotExist(missing_profile)
    assert isinstance(exc, ISortError)
