import pytest
from sty.primitive import Register
from collections import namedtuple

# Dummy RenderType class for testing
class DummyRenderType:
    pass

def test_eightbit_call_and_mute_behavior(tmp_path):
    reg = Register()
    # Register a dummy render function for DummyRenderType
    reg.set_renderfunc(DummyRenderType, lambda x: f"color{x}")
    # Set the eightbit call to use DummyRenderType
    reg.set_eightbit_call(DummyRenderType)
    # Normal call should use the render function
    assert reg(42) == "color42"
    # Muting the register should suppress output
    reg.mute()
    assert reg(42) == ""
    # Unmuting restores functionality
    reg.unmute()
    assert reg(42) == "color42"

def test_rgb_call_and_attribute_access(tmp_path):
    reg = Register()
    # Register a dummy render function for DummyRenderType
    reg.set_renderfunc(DummyRenderType, lambda r, g, b: f"rgb({r},{g},{b})")
    # Set the rgb call to use DummyRenderType
    reg.set_rgb_call(DummyRenderType)
    # RGB call should use the render function
    assert reg(10, 20, 30) == "rgb(10,20,30)"
    # Single string argument should return attribute value if exists
    reg.red = "redcode"
    assert reg("red") == "redcode"
    # Unknown attribute should return empty string
    assert reg("unknown") == ""

def test_as_dict_and_as_namedtuple(tmp_path):
    reg = Register()
    # Add some string attributes
    reg.red = "redcode"
    reg.green = "greencode"
    # as_dict should include only public string attributes
    d = reg.as_dict()
    assert isinstance(d, dict)
    assert d["red"] == "redcode"
    assert d["green"] == "greencode"
    # No private attributes should be present
    assert not any(k.startswith("_") for k in d)
    # as_namedtuple should produce a namedtuple with the same values
    nt = reg.as_namedtuple()
    assert isinstance(nt, namedtuple)
    assert nt.red == "redcode"
    assert nt.green == "greencode"
