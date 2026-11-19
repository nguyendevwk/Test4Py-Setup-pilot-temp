import pytest
from sty.lib import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass for testing purposes."""
    def __init__(self):
        self.muted = False

    def mute(self):
        self.muted = True


def test_mute_single_register(tmp_path):
    """Test that a single Register instance is muted."""
    reg = DummyRegister()
    assert not reg.muted
    mute(reg)
    assert reg.muted


def test_mute_multiple_registers(tmp_path):
    """Test that multiple Register instances are muted."""
    reg1 = DummyRegister()
    reg2 = DummyRegister()
    reg3 = DummyRegister()
    assert not reg1.muted and not reg2.muted and not reg3.muted
    mute(reg1, reg2, reg3)
    assert reg1.muted and reg2.muted and reg3.muted


def test_mute_no_arguments(tmp_path):
    """Test that calling mute with no arguments does nothing and returns None."""
    result = mute()
    assert result is None


def test_mute_invalid_argument_raises(tmp_path):
    """Test that passing a non-Register object raises ValueError."""
    class NotRegister:
        pass

    with pytest.raises(ValueError) as excinfo:
        mute(DummyRegister(), NotRegister())
    assert "The mute() method can only be used with objects that inherit" in str(excinfo.value)


def test_mute_mixed_valid_and_invalid(tmp_path):
    """Test that mute stops at the first invalid argument and raises."""
    reg = DummyRegister()
    class NotRegister:
        pass

    with pytest.raises(ValueError):
        mute(reg, NotRegister(), reg)  # second argument is invalid
    # Ensure that the first register was muted before the error
    assert reg.muted
