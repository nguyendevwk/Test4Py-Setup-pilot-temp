import pytest
from sty.primitive import Register
from collections import namedtuple

# Dummy RenderType class for testing
class DummyRenderType:
    pass

# Dummy render function that records its arguments
def dummy_render(*args, **kwargs):
    return f"rendered:{args}:{kwargs}"

def test_set_renderfunc_and_call_behavior(tmp_path):
    reg = Register()
    # Initially, no renderfuncs for DummyRenderType
    assert DummyRenderType not in reg.renderfuncs

    # Set a render function for DummyRenderType
    reg.set_renderfunc(DummyRenderType, dummy_render)
    assert reg.renderfuncs[DummyRenderType] is dummy_render

    # Set the eightbit and rgb calls to use the DummyRenderType
    reg.set_eightbit_call(DummyRenderType)
    reg.set_rgb_call(DummyRenderType)

    # Test eightbit call
    result_8bit = reg(42)
    assert result_8bit == "rendered:(42,):{}"

    # Test rgb call
    result_rgb = reg(10, 20, 30)
    assert result_rgb == "rendered:(10, 20, 30):{}"

    # Test that calling with a string returns attribute if exists
    reg.red = "red_value"
    assert reg("red") == "red_value"

    # Calling with unsupported number of args returns empty string
    assert reg(1, 2) == ""

def test_mute_and_unmute_behavior(tmp_path):
    reg = Register()
    reg.is_muted = False
    reg.some_attr = "visible"

    # Mute the register
    reg.mute()
    assert reg.is_muted is True
    # After muting, calling returns empty string
    assert reg(10) == ""

    # Unmute the register
    reg.unmute()
    assert reg.is_muted is False
    # After unmuting, calling returns the render function result
    reg.set_renderfunc(DummyRenderType, dummy_render)
    reg.set_eightbit_call(DummyRenderType)
    assert reg(10) == "rendered:(10,):{}"

def test_as_dict_and_as_namedtuple(tmp_path):
    reg = Register()
    reg.red = "red_value"
    reg.green = "green_value"
    reg._private = "should_not_appear"

    d = reg.as_dict()
    assert d == {"red": "red_value", "green": "green_value"}

    nt = reg.as_namedtuple()
    # namedtuple should have attributes red and green
    assert isinstance(nt, namedtuple("StyleRegister", ("red", "green")))
    assert nt.red == "red_value"
    assert nt.green == "green_value"
