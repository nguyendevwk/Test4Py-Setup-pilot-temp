import pytest
from pypara.commons.errors import ProgrammingError


def test_passert_no_exception_when_condition_true():
    """passert should not raise when the condition is True."""
    # No exception should be raised for a true condition
    ProgrammingError.passert(True, "This should not fail")
    # If we reach this point, the test passes


def test_passert_raises_default_message_on_false_condition():
    """passert should raise ProgrammingError with default message when condition is False."""
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(False)
    assert str(excinfo.value) == (
        "Broken coherence. Check your code against domain logic to fix it."
    )


def test_passert_raises_custom_message_on_false_condition():
    """passert should raise ProgrammingError with the provided custom message."""
    custom_msg = "Custom error message for debugging."
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(False, custom_msg)
    assert str(excinfo.value) == custom_msg
