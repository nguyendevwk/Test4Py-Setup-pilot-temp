import pytest
from copy import deepcopy
from collections import namedtuple

# Import the production code
from sty.primitive import Register, RenderType, Style, _render_rules
from typing import Callable, Dict, Type


# Helper RenderType subclasses
class DummyRender(RenderType):
    args: list = []


class DummyRender2(RenderType):
    args: list = []


def dummy_func(*args):
    return f"<{','.join(map(str, args))}>"


def dummy_func2(*args):
    return f"[{','.join(map(str, args))}]"


@pytest.fixture
def reg():
    """Create a Register with two dummy render functions."""
    r = Register()
    r.set_renderfunc(DummyRender, dummy_func)
    r.set_renderfunc(DummyRender2, dummy_func2)
    return r


def test_setattr_renders_style_and_mute_behavior(reg):
    # Create a Style with a DummyRender rule
    style = Style(DummyRender(1, 2), value="dummy")
    # Assign to register attribute
    reg.foo = style
    # The attribute should be a Style instance with rendered value
    assert isinstance(reg.foo, Style)
    assert str(reg.foo) == "<1,2>"
    # Muting the register should render empty string
    reg.mute()
    reg.foo = style
    assert str(reg.foo) == ""


def test_call_single_int_calls_eightbit(reg):
    # Set eightbit call to DummyRender
    reg.set_eightbit_call(DummyRender)
    assert reg(42) == "<42>"
    # Changing to DummyRender2
    reg.set_eightbit_call(DummyRender2)
    assert reg(99) == "[99]"


def test_call_single_str_returns_attribute(reg):
    reg.bar = "baz"
    assert reg("bar") == "baz"
    # Non-existing attribute returns AttributeError
    with pytest.raises(AttributeError):
        reg("nonexistent")


def test_call_three_ints_calls_rgb(reg):
    reg.set_rgb_call(DummyRender)
    assert reg(1, 2, 3) == "<1,2,3>"
    reg.set_rgb_call(DummyRender2)
    assert reg(4, 5, 6) == "[4,5,6]"


def test_set_renderfunc_updates_existing_style(reg):
    # Initially foo uses DummyRender
    style = Style(DummyRender(7), value="dummy")
    reg.foo = style
    assert str(reg.foo) == "<7>"
    # Replace render function
    reg.set_renderfunc(DummyRender, dummy_func2)
    # Existing attribute should re-render with new function
    assert str(reg.foo) == "[7]"


def test_mute_and_unmute(reg):
    style = Style(DummyRender(8), value="dummy")
    reg.foo = style
    assert str(reg.foo) == "<8>"
    reg.mute()
    assert reg.foo == ""
    reg.unmute()
    assert str(reg.foo) == "<8>"


def test_as_dict_and_namedtuple(reg):
    reg.red = "<red>"
    reg.green = "<green>"
    d = reg.as_dict()
    assert d["red"] == "<red>"
    assert d["green"] == "<green>"
    nt = reg.as_namedtuple()
    assert isinstance(nt, namedtuple)
    assert getattr(nt, "red") == "<red>"
    assert getattr(nt, "green") == "<green>"


def test_copy_deepcopy(reg):
    reg.foo = Style(DummyRender(9), value="dummy")
    reg_copy = reg.copy()
    # Ensure deep copy: modifying copy does not affect original
    reg_copy.foo = Style(DummyRender(10), value="dummy")
    assert str(reg.foo) == "<9>"
    assert str(reg_copy.foo) == "<10>"


def test_render_rules_raises_on_invalid_rule():
    with pytest.raises(ValueError):
        _render_rules({}, [object()])  # invalid rule type
