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


def test_mute_single_register():
    """Mute a single Register instance and verify the mute flag is set."""
    reg = DummyRegister()
    assert not reg.muted, "Register should start unmuted"
    mute(reg)
    assert reg.muted, "Register.mute() should set muted to True"


def test_mute_multiple_registers():
    """Mute multiple Register instances in one call."""
    reg1 = DummyRegister()
    reg2 = DummyRegister()
    reg3 = DummyRegister()
    mute(reg1, reg2, reg3)
    assert all(r.muted for r in (reg1, reg2, reg3)), "All registers should be muted"


def test_mute_invalid_argument_raises():
    """Passing a non-Register object should raise ValueError."""
    class NotRegister:
        pass

    with pytest.raises(ValueError) as excinfo:
        mute(DummyRegister(), NotRegister())
    assert "inherit from the 'Register class'" in str(excinfo.value)
