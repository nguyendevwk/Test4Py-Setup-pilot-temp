import pytest
from sty.lib import mute
from sty.primitive import Register, Style


def test_mute_multiple_registers(tmp_path):
    """Muting multiple Register objects should set their is_muted flag."""
    reg1 = Register()
    reg2 = Register()

    # Ensure initial state
    assert not reg1.is_muted
    assert not reg2.is_muted

    # Assign a style attribute to verify it remains accessible after mute
    reg1.red = Style("red", value="\x1b[31m")
    reg2.green = Style("green", value="\x1b[32m")

    mute(reg1, reg2)

    # After mute, is_muted should be True
    assert reg1.is_muted
    assert reg2.is_muted

    # The style attributes should still exist but calling them should return empty string
    assert isinstance(reg1.red, Style)
    assert isinstance(reg2.green, Style)
    assert reg1.red() == ""
    assert reg2.green() == ""


def test_mute_single_register(tmp_path):
    """Muting a single Register object should work as expected."""
    reg = Register()
    reg.blue = Style("blue", value="\x1b[34m")

    mute(reg)

    assert reg.is_muted
    assert reg.blue() == ""


def test_mute_no_arguments():
    """Calling mute with no arguments should not raise an exception."""
    # No exception should be raised
    mute()


def test_mute_invalid_argument():
    """Passing a non-Register object should raise ValueError."""
    class Dummy:
        pass

    dummy = Dummy()
    with pytest.raises(ValueError) as excinfo:
        mute(dummy)

    assert (
        "The mute() method can only be used with objects that inherit "
        "from the 'Register class'."
        in str(excinfo.value)
    )


def test_mute_preserves_other_attributes(tmp_path):
    """Muting should not alter non-Style attributes."""
    reg = Register()
    reg.some_int = 42
    reg.some_str = "hello"

    mute(reg)

    assert reg.is_muted
    assert reg.some_int == 42
    assert reg.some_str == "hello"


def test_mute_repeated_calls(tmp_path):
    """Calling mute multiple times should keep the object muted."""
    reg = Register()
    mute(reg)
    assert reg.is_muted
    mute(reg)
    assert reg.is_muted
