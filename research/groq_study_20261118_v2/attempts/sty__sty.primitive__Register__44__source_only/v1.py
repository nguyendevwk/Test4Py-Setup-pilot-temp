import pytest
from copy import deepcopy
from collections import namedtuple
from sty.primitive import Register
from sty.rendertype import RenderType

# Dummy RenderType subclasses for testing
class DummyRenderType(RenderType):
    pass

class AnotherRenderType(RenderType):
    pass

# Simple render functions that return identifiable strings
def dummy_render_func(value):
    return f"DUMMY({value})"

def another_render_func(r, g, b):
    return f"ANOTHER({r},{g},{b})"

@pytest.fixture
def reg():
    """Create a Register instance with dummy render functions."""
    r = Register()
    r.set_renderfunc(DummyRenderType, dummy_render_func)
    r.set_renderfunc(AnotherRenderType, another_render_func)
    # Assign a dummy attribute that will be rendered
    r.foo = DummyRenderType
    return r

def test_call_single_int_calls_eightbit(reg):
    # By default, eightbit_call is identity; set to dummy_render_func
    reg.set_eightbit_call(DummyRenderType)
    assert reg(42) == "DUMMY(42)"

def test_call_single_str_returns_attribute(reg):
    # Attribute foo should be the class DummyRenderType
    assert reg("foo") == DummyRenderType

def test_call_three_ints_calls_rgb(reg):
    reg.set_rgb_call(AnotherRenderType)
    assert reg(10, 20, 30) == "ANOTHER(10,20,30)"

def test_call_invalid_length_returns_empty(reg):
    assert reg() == ""
    assert reg(1, 2) == ""

def test_mute_and_unmute(reg):
    # Muted register should return empty string for any call
    reg.mute()
    assert reg(42) == ""
    assert reg("foo") == ""
    assert reg(1, 2, 3) == ""

    # Unmuting restores original behavior
    reg.unmute()
    reg.set_eightbit_call(DummyRenderType)
    assert reg(42) == "DUMMY(42)"
    reg.set_rgb_call(AnotherRenderType)
    assert reg(1, 2, 3) == "ANOTHER(1,2,3)"

def test_set_renderfunc_updates_attributes(reg):
    # Initially foo uses DummyRenderType
    assert reg("foo") == DummyRenderType

    # Replace DummyRenderType with AnotherRenderType
    reg.set_renderfunc(DummyRenderType, another_render_func)
    # After update, foo should now be the class DummyRenderType (unchanged)
    assert reg("foo") == DummyRenderType

def test_as_dict_and_namedtuple(reg):
    # as_dict should include 'foo' key with the class object
    d = reg.as_dict()
    assert "foo" in d
    assert d["foo"] == DummyRenderType

    # as_namedtuple should produce a namedtuple with same values
    nt = reg.as_namedtuple()
    assert hasattr(nt, "foo")
    assert getattr(nt, "foo") == d["foo"]

def test_copy_is_deepcopy(reg):
    reg_copy = reg.copy()
    # Modifying the copy should not affect the original
    reg_copy.set_eightbit_call(DummyRenderType)
    assert reg_copy(42) == "DUMMY(42)"
    assert reg(42) == "DUMMY(42)"

    # Ensure the copy is a distinct object
    assert reg_copy is not reg
    assert isinstance(reg_copy, Register)
