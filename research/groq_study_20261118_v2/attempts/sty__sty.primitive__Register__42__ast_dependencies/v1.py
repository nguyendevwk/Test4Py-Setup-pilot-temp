import pytest
from sty.primitive import Register, Style, RenderType, _render_rules

# --------------------------------------------------------------------------- #
# Helper RenderType subclasses that accept arguments
# --------------------------------------------------------------------------- #
class DummyRender(RenderType):
    def __init__(self, *args):
        self.args = list(args)

class DummyRender2(RenderType):
    def __init__(self, *args):
        self.args = list(args)

# --------------------------------------------------------------------------- #
# Dummy render functions
# --------------------------------------------------------------------------- #
def render_func_1(*args):
    return f"<{args}>"

def render_func_2(*args):
    return f"[{args}]"

# --------------------------------------------------------------------------- #
# Fixture that creates a Register with dummy render functions and a style
# --------------------------------------------------------------------------- #
@pytest.fixture
def register():
    reg = Register()
    reg.set_renderfunc(DummyRender, render_func_1)
    reg.set_renderfunc(DummyRender2, render_func_2)
    reg.red = Style(DummyRender(1), value="red")
    return reg

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_setattr_and_rendering(register):
    assert isinstance(register.red, Style)
    assert str(register.red) == "<(1,)>"
    register.set_renderfunc(DummyRender, lambda *a: f"{{{a}}}")
    assert str(register.red) == "{(1,)}"

def test_mute_and_unmute(register):
    register.mute()
    assert register.red == ""
    register.unmute()
    assert str(register.red) == "<(1,)>"

def test_call_single_int(register):
    register.set_eightbit_call(DummyRender)
    assert register(42) == "<(42,)>"

def test_call_single_str(register):
    assert register("red") == "<(1,)>"

def test_call_three_ints(register):
    register.set_rgb_call(DummyRender2)
    assert register(10, 20, 30) == "[(10, 20, 30)]"

def test_call_invalid_args(register):
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
    assert reg_copy is not register
    reg_copy.mute()
    assert reg_copy.red == ""
    assert register.red == "<(1,)>"

def test_render_rules_function():
    nested_style = Style(
        Style(DummyRender(5), value="inner"),
        DummyRender2(6),
        value="outer",
    )
    rendered, flattened = _render_rules(
        {DummyRender: render_func_1, DummyRender2: render_func_2},
        nested_style.rules,
    )
    assert rendered == "<(5,)><(6,)>"
    assert flattened == (
        Style(DummyRender(5), value="inner"),
        DummyRender2(6),
    )

def test_set_renderfunc_updates_existing_style(register):
    register.set_renderfunc(DummyRender, lambda *a: f"NEW{a}")
    assert str(register.red) == "NEW(1,)"

def test_as_dict_excludes_private_and_non_str(register):
    register._private = "secret"
    register.number = 42
    d = register.as_dict()
    assert "_private" not in d
    assert "number" not in d
    assert "red" in d
