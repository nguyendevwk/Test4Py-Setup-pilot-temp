import pytest
from sty.primitive import Register, Style
from sty.lib import mute


def test_mute_sets_is_muted_and_updates_attributes(tmp_path):
    # Create a register and add a style attribute
    reg = Register()
    reg.foo = Style(value="FOO")  # use empty rules to avoid rendering error
    # Ensure attribute is a Style instance
    assert isinstance(reg.foo, Style)
    # Mute the register
    mute(reg)
    # is_muted flag should be True
    assert reg.is_muted is True
    # The attribute should still be a Style instance but its value should be empty
    assert isinstance(reg.foo, Style)
    assert str(reg.foo) == ""  # muted styles render to empty string


def test_mute_multiple_registers():
    reg1 = Register()
    reg2 = Register()
    reg1.foo = Style(value="FOO")
    reg2.bar = Style(value="BAR")
    mute(reg1, reg2)
    assert reg1.is_muted is True
    assert reg2.is_muted is True
    assert str(reg1.foo) == ""
    assert str(reg2.bar) == ""


def test_mute_with_non_register_raises_value_error():
    class Dummy:
        pass

    dummy = Dummy()
    reg = Register()
    with pytest.raises(ValueError) as excinfo:
        mute(reg, dummy)
    # The error message should match the one defined in mute()
    assert (
        str(excinfo.value)
        == "The mute() method can only be used with objects that inherit from the 'Register class'."
    )
    # The valid register should remain muted because the exception stops the loop
    assert reg.is_muted is True


def test_mute_is_idempotent_and_respects_unmute():
    reg = Register()
    reg.foo = Style(value="FOO")
    mute(reg)
    # Muting again should not raise an error and keep the state
    mute(reg)
    assert reg.is_muted is True
    # Unmute and check that styles render again
    reg.unmute()
    assert reg.is_muted is False
    assert str(reg.foo) == "FOO"


def test_mute_does_not_affect_non_style_attributes():
    reg = Register()
    reg.some_int = 42
    reg.some_str = "hello"
    mute(reg)
    # Non-Style attributes should remain unchanged
    assert reg.some_int == 42
    assert reg.some_str == "hello"
