import pytest
from sty.lib import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass for testing purposes."""

    def __init__(self):
        self.muted = False

    def mute(self):
        """Mark the register as muted."""
        self.muted = True


def test_mute_with_single_register(tmp_path):
    """Test that a single Register object is muted correctly."""
    reg = DummyRegister()
    assert not reg.muted, "Register should start unmuted."
    mute(reg)
    assert reg.muted, "Register should be muted after calling mute()."


def test_mute_with_multiple_registers(tmp_path):
    """Test that multiple Register objects are muted correctly."""
    regs = [DummyRegister() for _ in range(3)]
    for reg in regs:
        assert not reg.muted, "Each register should start unmuted."
    mute(*regs)
    for reg in regs:
        assert reg.muted, "Each register should be muted after calling mute()."


def test_mute_with_no_arguments():
    """Test that calling mute() with no arguments does nothing and raises no error."""
    # No exception should be raised
    mute()


def test_mute_with_invalid_argument_raises_value_error():
    """Test that passing a non-Register object raises a ValueError."""
    class NotARegister:
        pass

    with pytest.raises(ValueError) as excinfo:
        mute(DummyRegister(), NotARegister())
    assert (
        "The mute() method can only be used with objects that inherit "
        "from the 'Register class'." in str(excinfo.value)
    ), "Error message should match the expected text."


def test_mute_with_mixed_valid_and_invalid_objects():
    """Test that mute() raises an error when any argument is invalid, even if others are valid."""
    reg = DummyRegister()
    class AnotherInvalid:
        pass

    with pytest.raises(ValueError):
        mute(reg, AnotherInvalid())
