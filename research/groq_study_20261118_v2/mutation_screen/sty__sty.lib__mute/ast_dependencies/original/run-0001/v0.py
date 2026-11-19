import pytest
from sty.lib import mute
from sty.primitive import Register, Style


def test_mute_multiple_registers(tmp_path):
    """Muting several Register objects should set their is_muted flag."""
    reg1 = Register()
    reg2 = Register()
    # Attach a dummy style to ensure attributes are present
    reg1.foo = Style("foo")
    reg2.bar = Style("bar")

    mute(reg1, reg2)

    assert reg1.is_muted is True
    assert reg2.is_muted is True
    # Styles should still be accessible but return empty string when called
    assert reg1.foo == Style("foo")  # style object unchanged
    assert reg2.bar == Style("bar")
    # Calling the register should return empty string because it is muted
    assert reg1() == ""
    assert reg2() == ""


def test_mute_no_arguments():
    """Calling mute with no arguments should simply return None."""
    result = mute()
    assert result is None


def test_mute_invalid_argument():
    """Passing a non-Register object should raise ValueError."""
    class Dummy:
        pass

    dummy = Dummy()
    with pytest.raises(ValueError) as excinfo:
        mute(dummy)
    assert "The mute() method can only be used with objects that inherit" in str(excinfo.value)


def test_mute_unmute_behavior(tmp_path):
    """After muting, unmuting should restore original behavior."""
    reg = Register()
    reg.foo = Style("foo")
    mute(reg)
    assert reg.is_muted is True
    # Muted register returns empty string
    assert reg() == ""
    # Unmute and check again
    reg.unmute()
    assert reg.is_muted is False
    # Now calling register should return something non-empty
    assert reg() != ""


def test_mute_preserves_style_rules(tmp_path):
    """Styles attached to a register should retain their rules after muting."""
    reg = Register()
    reg.red = Style("red")
    reg.green = Style("green")
    mute(reg)
    # The style objects should still have the same rules
    assert reg.red.rules == ("red",)
    assert reg.green.rules == ("green",)
    # Muted register returns empty string
    assert reg() == ""
