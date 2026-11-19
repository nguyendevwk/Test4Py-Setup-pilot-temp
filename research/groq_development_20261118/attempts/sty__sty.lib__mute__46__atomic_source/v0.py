import pytest
from sty.lib.mute import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass that records mute calls."""
    def __init__(self):
        super().__init__()
        self.muted = False

    def mute(self):
        self.muted = True


def test_mute_multiple_registers_calls_mute():
    """mute() should call mute() on each Register instance passed."""
    r1 = DummyRegister()
    r2 = DummyRegister()
    mute(r1, r2)
    assert r1.muted is True, "First register was not muted"
    assert r2.muted is True, "Second register was not muted"


def test_mute_no_arguments_does_nothing():
    """mute() with no arguments should not raise and perform no action."""
    # No exception should be raised
    mute()
    # Nothing to assert on state, just ensure no error


def test_mute_with_invalid_argument_raises_value_error():
    """mute() should raise ValueError if any argument is not a Register."""
    class NotRegister:
        pass

    with pytest.raises(ValueError) as excinfo:
        mute(DummyRegister(), NotRegister())
    assert "The mute() method can only be used with objects that inherit" in str(excinfo.value)
