import pytest
from collections import namedtuple
from sty.primitive import Register
from sty.rendertype import RenderType

# Dummy RenderType subclasses for testing
class Dummy8bit(RenderType):
    pass

class Dummy24bit(RenderType):
    pass

# Simple render functions that return identifiable strings
def render8bit(value):
    return f"8bit:{value}"

def render24bit(r, g, b):
    return f"24bit:{r},{g},{b}"

def test_register_call_and_render_functions(tmp_path):
    reg = Register()
    # Register render functions
    reg.set_renderfunc(Dummy8bit, render8bit)
    reg.set_renderfunc(Dummy24bit, render24bit)

    # Set the call handlers
    reg.set_eightbit_call(Dummy8bit)
    reg.set_rgb_call(Dummy24bit)

    # 8‑bit call returns expected string
    assert reg(42) == "8bit:42"
    # 24‑bit call returns expected string
    assert reg(10, 20, 30) == "24bit:10,20,30"

    # Attribute lookup via string name
    reg.red = "red_value"
    assert reg("red") == "red_value"

    # Wrong number of args returns empty string
    assert reg(1, 2) == ""

def test_register_mute_and_unmute_behavior():
    reg = Register()
    reg.set_renderfunc(Dummy8bit, render8bit)
    reg.set_eightbit_call(Dummy8bit)

    # Muted: calls return empty string
    reg.mute()
    assert reg(5) == ""
    # Unmuted: calls return rendered string
    reg.unmute()
    assert reg(5) == "8bit:5"

def test_register_as_dict_and_namedtuple():
    reg = Register()
    reg.set_renderfunc(Dummy8bit, render8bit)
    reg.set_eightbit_call(Dummy8bit)

    # Define some attributes
    reg.foo = "foo_value"
    reg.bar = "bar_value"

    # as_dict should contain only public string attributes
    d = reg.as_dict()
    assert d == {"foo": "foo_value", "bar": "bar_value"}

    # as_namedtuple should produce a namedtuple with same values
    nt = reg.as_namedtuple()
    assert isinstance(nt, namedtuple("StyleRegister", ("foo", "bar")))
    assert nt.foo == "foo_value"
    assert nt.bar == "bar_value"
