import pytest
from isort.exceptions import ProfileDoesNotExist
from isort.profiles import profiles


def test_profile_does_not_exist_message_contains_profile_and_available():
    """The error message should mention the missing profile and list all available profiles."""
    missing = "nonexistent_profile"
    exc = ProfileDoesNotExist(missing)
    assert missing in str(exc), "Missing profile name not in error message"
    for p in profiles:
        assert p in str(exc), f"Profile '{p}' not listed in error message"


def test_profile_does_not_exist_attribute_set():
    """The ProfileDoesNotExist instance should expose the missing profile via the `profile` attribute."""
    missing = "another_missing"
    exc = ProfileDoesNotExist(missing)
    assert exc.profile == missing, "The `profile` attribute does not match the input"


def test_profile_does_not_exist_inherits_from_ISortError():
    """ProfileDoesNotExist should be a subclass of ISortError and behave like an exception."""
    missing = "yet_another_missing"
    exc = ProfileDoesNotExist(missing)
    # ISortError is defined in isort.exceptions; ensure isinstance works
    from isort.exceptions import ISortError
    assert isinstance(exc, ISortError), "ProfileDoesNotExist is not an ISortError"
    # Raising and catching the exception should work as expected
    with pytest.raises(ISortError) as ctx:
        raise exc
    assert ctx.value is exc, "Raised exception is not the same instance"
