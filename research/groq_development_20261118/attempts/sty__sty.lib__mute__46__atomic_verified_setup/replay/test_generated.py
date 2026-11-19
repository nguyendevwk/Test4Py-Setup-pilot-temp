import pytest
from sty.lib import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass that records whether mute was called."""
    def __init__(self):
        super().__init__()
        self.muted = False

    def mute(self):
        self.muted = True


def test_mute_multiple_registers_calls_mute():
    """When multiple Register instances are passed, each should have mute() called."""
    r1 = DummyRegister()
    r2 = DummyRegister()
    r3 = DummyRegister()

    mute(r1, r2, r3)

    assert r1.muted is True, "r1.mute() was not called"
    assert r2.muted is True, "r2.mute() was not called"
    assert r3.muted is True, "r3.mute() was not called"


def test_mute_no_arguments_does_not_raise():
    """Calling mute with no arguments should simply return without error."""
    # No exception should be raised
    mute()


def test_mute_invalid_argument_raises_value_error():
    """Passing a non-Register object should raise a ValueError with the correct message."""
    class NotRegister:
        pass

    with pytest.raises(ValueError) as excinfo:
        mute(DummyRegister(), NotRegister())

    assert str(excinfo.value) == (
        "The mute() method can only be used with objects that inherit "
        "from the 'Register class'."
    )
