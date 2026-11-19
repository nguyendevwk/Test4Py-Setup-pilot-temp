import pytest
from copy import deepcopy
from types import SimpleNamespace

# Import the production code
from sty.primitive import Register, Style, RenderType, _render_rules

# Helper RenderType subclasses for testing
class DummyRender(RenderType):
    args: list = []

class DummyRender2(RenderType):
    args: list = []

# Dummy render functions
def render_func_1(*args):
    return f"<{args}>"

def render_func_2(*args):
    return f"[{args}]"

@pytest.fixture
def register():
    reg = Register()
    # Attach dummy render functions
    reg.set_renderfunc(DummyRender, render_func_1)
    reg.set_renderfunc(DummyRender2, render_func_2)
    # Define a style attribute
    reg.red = Style(DummyRender(1), value="red")
    return reg

def test_setattr_and_rendering(register):
    # The attribute should be a Style instance with rendered value
    assert isinstance(register.red, Style)
    assert str(register.red) == "<(1,)>"
    # Changing the underlying render function should update the attribute
    register.set_renderfunc(DummyRender, lambda *a: f"{{{a}}}")
    assert str(register.red) == "{(1,)}"

def test_mute_and_unmute(register):
    # Muted register returns empty string for any style
    register.mute()
    assert register.red == ""
    # Unmuted restores original rendering
    register.unmute()
    assert str(register.red) == "<(1,)>"

def test_call_single_int(register):
    # Single int argument triggers eightbit_call
    register.set_eightbit_call(DummyRender)
    assert register(42) == "<(42,)>"

def test_call_single_str(register):
    # Single string argument returns attribute value
    assert register("red") == "<(1,)>"

def test_call_three_ints(register):
    # Three ints trigger rgb_call
    register.set_rgb_call(DummyRender2)
    assert register(10, 20, 30) == "[(10, 20, 30)]"

def test_call_invalid_args(register):
    # Any other number of args returns empty string
    assert register() == ""
    assert register(1, 2) == ""

def test_as_dict_and_namedtuple(register):
    d = register.as_dict()
    assert "red" in d
    assert d["red"] == "<(1,)>"
    nt = register.as_namedtuple()
    assert hasattr(nt, "red")
    assert getattr(nt, "red") == "<(1,)>"

def test_copy_deepcopy(register):
    reg_copy = register.copy()
    # The copy should be a distinct object
    assert reg_copy is not register
    # Mutating the copy should not affect the original
    reg_copy.mute()
    assert reg_copy.red == ""
    assert register.red == "<(1,)>"

def test_render_rules_function():
    # Test that _render_rules correctly processes nested styles
    nested_style = Style(Style(DummyRender(5), value="inner"), DummyRender2(6), value="outer")
    rendered, flattened = _render_rules(
        {DummyRender: render_func_1, DummyRender2: render_func_2},
        nested_style.rules,
    )
    assert rendered == "<(5,)><(6,)>"
    # Flattened should contain the original rules in order
    assert flattened == (Style(DummyRender(5), value="inner"), DummyRender2(6))

def test_set_renderfunc_updates_existing_style(register):
    # Add a new render function and ensure existing style updates
    register.set_renderfunc(DummyRender, lambda *a: f"NEW{a}")
    assert str(register.red) == "NEW(1,)"

def test_set_renderfunc_with_non_style_attribute():
    # Adding a non-Style attribute should not raise
    register.foo = 123
    register.set_renderfunc(DummyRender, lambda *a: f"NEW{a}")
    # Existing style still updated
    assert str(register.red) == "NEW(1,)"

def test_as_dict_excludes_private_and_non_str():
    register._private = "secret"
    register.number = 42
    d = register.as_dict()
    assert "_private" not in d
    assert "number" not in d
    assert "red" in d
