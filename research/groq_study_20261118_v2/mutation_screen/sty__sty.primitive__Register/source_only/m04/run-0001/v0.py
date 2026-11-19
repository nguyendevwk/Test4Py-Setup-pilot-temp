import pytest
from copy import deepcopy
from collections import namedtuple

# Import the Register class from the production module
from sty.primitive import Register


class DummyRenderType:
    """A simple dummy RenderType used for testing."""
    pass


def dummy_render_func(*args, **kwargs):
    """Return a string representation of the arguments for testing."""
    return f"rendered:{args}:{kwargs}"


def test_call_behavior_with_muted_and_unmuted():
    reg = Register()

    # Initially not muted: calling with a single int should use eightbit_call
    reg.set_eightbit_call(DummyRenderType)
    reg.renderfuncs[DummyRenderType] = dummy_render_func
    result = reg(42)
    assert result == "rendered:(42,):{}"

    # Calling with a single string should return the attribute value
    reg.foo = "bar"
    assert reg("foo") == "bar"

    # Calling with three ints should use rgb_call
    reg.set_rgb_call(DummyRenderType)
    reg.renderfuncs[DummyRenderType] = dummy_render_func
    assert reg(10, 20, 30) == "rendered:(10, 20, 30):{}"

    # Any other number of args returns empty string
    assert reg() == ""
    assert reg(1, 2) == ""

    # Muting the register should make all calls return empty string
    reg.mute()
    assert reg(42) == ""
    assert reg("foo") == ""
    assert reg(10, 20, 30) == ""

    # Unmuting restores original behavior
    reg.unmute()
    assert reg(42) == "rendered:(42,):{}"
    assert reg("foo") == "bar"
    assert reg(10, 20, 30) == "rendered:(10, 20, 30):{}"


def test_set_renderfunc_updates_render_functions_and_attributes():
    reg = Register()

    # Set a new render function and verify it is stored
    reg.set_renderfunc(DummyRenderType, dummy_render_func)
    assert reg.renderfuncs[DummyRenderType] is dummy_render_func

    # Assign a string attribute and ensure it remains unchanged
    reg.some_attr = "value"
    assert reg.some_attr == "value"

    # Assign a non-string attribute and ensure it remains unchanged
    reg.number_attr = 123
    assert reg.number_attr == 123


def test_as_dict_and_as_namedtuple_exports():
    reg = Register()
    reg.red = "red"
    reg.green = "green"
    reg._private = "should_not_appear"

    # as_dict should only include public string attributes
    d = reg.as_dict()
    assert isinstance(d, dict)
    assert d == {"red": "red", "green": "green"}
    assert "_private" not in d

    # as_namedtuple should create a namedtuple with the same fields
    nt = reg.as_namedtuple()
    assert isinstance(nt, namedtuple)
    assert nt._fields == ("red", "green")
    assert nt.red == "red"
    assert nt.green == "green"


def test_copy_creates_deepcopy_and_is_independent():
    reg = Register()
    reg.red = "red"

    reg_copy = reg.copy()
    assert reg_copy is not reg
    assert reg_copy.red == "red"

    # Mutating the copy should not affect the original
    reg_copy.red = "blue"
    assert reg_copy.red == "blue"
    assert reg.red == "red"

    # Mutating the original should not affect the copy
    reg.red = "green"
    assert reg.red == "green"
    assert reg_copy.red == "blue"
