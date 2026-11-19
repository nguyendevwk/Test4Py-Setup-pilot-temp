import pytest
from pypara.commons.errors import ProgrammingError


def test_passert_passes_without_exception():
    """passert should not raise when the condition is True."""
    # No exception should be raised for a true condition
    ProgrammingError.passert(True, "This should not fail")


def test_passert_raises_default_message():
    """passert should raise ProgrammingError with default message when condition is False."""
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(False)
    assert str(excinfo.value) == (
        "Broken coherence. Check your code against domain logic to fix it."
    )


def test_passert_raises_custom_message():
    """passert should raise ProgrammingError with the provided custom message."""
    custom_msg = "Custom error message"
    with pytest.raises(ProgrammingError) as excinfo:
        ProgrammingError.passert(False, custom_msg)
    assert str(excinfo.value) == custom_msg
