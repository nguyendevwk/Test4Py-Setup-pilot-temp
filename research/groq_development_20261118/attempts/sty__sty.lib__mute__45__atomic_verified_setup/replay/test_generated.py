import pytest
from sty.lib import mute
from sty.primitive import Register


class DummyRegister(Register):
    """A minimal Register subclass that records when mute is called."""

    def __init__(self):
        super().__init__()
        self.muted = False

    def mute(self):
        self.muted = True


def test_mute_single_register():
    """mute should call mute() on a single Register instance."""
    reg = DummyRegister()
    assert not reg.muted, "Register should start unmuted"
    mute(reg)
    assert reg.muted, "mute() should set the muted flag to True"


def test_mute_multiple_registers_and_no_args():
    """mute should handle multiple Register instances and no arguments gracefully."""
    reg1 = DummyRegister()
    reg2 = DummyRegister()
    # No arguments: should not raise
    mute()
    # Multiple arguments: all should be muted
    mute(reg1, reg2)
    assert reg1.muted and reg2.muted, "All provided registers should be muted"


def test_mute_invalid_argument_raises():
    """mute should raise ValueError when a non-Register object is passed."""
    with pytest.raises(ValueError) as excinfo:
        mute("not a register")
    assert "inherit from the 'Register class'" in str(excinfo.value)
