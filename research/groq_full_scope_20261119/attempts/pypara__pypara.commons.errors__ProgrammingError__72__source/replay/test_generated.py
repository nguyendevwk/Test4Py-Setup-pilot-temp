import pytest
from pypara.commons.errors import ProgrammingError


def test_passert_no_exception_when_condition_true():
    """passert should not raise when the condition is True."""
    # No exception should be raised for a true condition
    ProgrammingError.passert(1 == 1)
    # If no exception is raised, the test passes


def test_passert_raises_default_message_when_condition_false():
    """passert should raise ProgrammingError with default message when condition is False."""
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(1 == 0)
    # Assert that the exception message matches the default
    assert str(excinfo.value) == (
        "Broken coherence. Check your code against domain logic to fix it."
    )


def test_passert_raises_custom_message_when_condition_false():
    """passert should raise ProgrammingError with the provided custom message."""
    custom_msg = "Custom error: invalid state detected."
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(False, custom_msg)
    # Assert that the exception message matches the custom message
    assert str(excinfo.value) == custom_msg
