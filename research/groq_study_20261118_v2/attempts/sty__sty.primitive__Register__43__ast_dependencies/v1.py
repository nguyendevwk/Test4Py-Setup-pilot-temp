import pytest
from copy import deepcopy
from types import SimpleNamespace

# Import the production Register and related classes
from sty.primitive import Register, Style, RenderType, _render_rules
from typing import Callable, Dict, Type

# --------------------------------------------------------------------------- #
# Helper render functions and dummy RenderTypes
# --------------------------------------------------------------------------- #

class DummyRenderType(RenderType):
    """A simple RenderType that stores its args."""
    def __init__(self, *args):
        self.args = list(args)

def dummy_render_func(*args: int) -> str:
    """Return a deterministic ANSI-like string for testing."""
    return f"<{','.join(map(str, args))}>"

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

@pytest.fixture
def register() -> Register:
    """Create a Register with a dummy render function for DummyRenderType."""
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_render_func)
    return reg

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_setattr_renders_style_when_not_muted(register: Register):
    """Assigning a Style should render its rules into a string."""
    # Create a Style that contains a DummyRenderType
    style = Style(DummyRenderType(1, 2, 3), value="")  # value ignored
    register.foo = style
    # After assignment, the attribute should be a Style instance with rendered value
    assert isinstance(register.foo, Style)
    assert str(register.foo) == "<1,2,3>"
    # The rules should be preserved
    assert register.foo.rules == (DummyRenderType(1, 2, 3),)

def test_setattr_does_not_render_when_muted(register: Register):
    """When muted, the Style is stored without rendering."""
    register.mute()
    style = Style(DummyRenderType(4, 5, 6), value="")
    register.bar = style
    # The stored value should be empty string
    assert str(register.bar) == ""
    # The rules should still be present
    assert register.bar.rules == (DummyRenderType(4, 5, 6),)
    register.unmute()

def test_call_single_int_returns_eightbit_call(register: Register):
    """Calling the register with a single int uses the eightbit_call."""
    # Set a custom eightbit_call that records the argument
    called = {}
    def eightbit(x):
        called['x'] = x
        return f"8bit:{x}"
    register.set_eightbit_call(DummyRenderType)
    register.eightbit_call = eightbit
    result = register(42)
    assert result == "8bit:42"
    assert called['x'] == 42

def test_call_single_str_returns_attribute(register: Register):
    """Calling the register with a single string returns the attribute."""
    register.red = Style(DummyRenderType(9, 9, 9), value="")
    assert register("red") == "<9,9,9>"

def test_call_three_ints_returns_rgb_call(register: Register):
    """Calling the register with three ints uses the rgb_call."""
    called = {}
    def rgb(r, g, b):
        called['rgb'] = (r, g, b)
        return f"rgb:{r},{g},{b}"
    register.set_rgb_call(DummyRenderType)
    register.rgb_call = rgb
    result = register(10, 20, 30)
    assert result == "rgb:10,20,30"
    assert called['rgb'] == (10, 20, 30)

def test_call_muted_returns_empty_string(register: Register):
    """When muted, any call returns an empty string."""
    register.mute()
    assert register(1) == ""
    assert register("foo") == ""
    register.unmute()

def test_set_renderfunc_updates_existing_styles(register: Register):
    """Changing the render function should re-render existing Style attributes."""
    # Initially use dummy_render_func
    style = Style(DummyRenderType(7, 8, 9), value="")
    register.green = style
    assert register.green == "<7,8,9>"
    # Replace render function with a new one
    def new_render(*args):
        return f"NEW:{','.join(map(str, args))}"
    register.set_renderfunc(DummyRenderType, new_render)
    # Existing attribute should be re-rendered
    assert register.green == "NEW:7,8,9"

def test_mute_and_unmute_re_render(register: Register):
    """Muting and unmuting should re-render all Style attributes."""
    style = Style(DummyRenderType(1, 1, 1), value="")
    register.yellow = style
    assert register.yellow == "<1,1,1>"
    register.mute()
    assert register.yellow == ""
    register.unmute()
    assert register.yellow == "<1,1,1>"

def test_as_dict_and_as_namedtuple(register: Register):
    """Exporting the register as dict and namedtuple works correctly."""
    register.blue = Style(DummyRenderType(0, 0, 1), value="")
    register.green = Style(DummyRenderType(0, 1, 0), value="")
    d = register.as_dict()
    assert d == {"blue": "<0,0,1>", "green": "<0,1,0>"}
    nt = register.as_namedtuple()
    assert hasattr(nt, "blue") and hasattr(nt, "green")
    assert nt.blue == "<0,0,1>"
    assert nt.green == "<0,1,0>"

def test_copy_is_deepcopy(register: Register):
    """Copying a register yields an independent deepcopy."""
    register.red = Style(DummyRenderType(9, 9, 9), value="")
    copy_reg = register.copy()
    # Mutate the copy
    copy_reg.red = Style(DummyRenderType(1, 1, 1), value="")
    # Original should remain unchanged
    assert register.red == "<9,9,9>"
    assert copy_reg.red == "<1,1,1>"

def test_render_rules_raises_on_invalid_rule():
    """_render_rules should raise ValueError for unsupported rule types."""
    with pytest.raises(ValueError, match="Parameter 'rules' must be of type Iterable\\[Rule\\]."):
        _render_rules({}, [123])  # 123 is not a Style or RenderType
