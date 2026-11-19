import pytest
from sty.primitive import Register
from sty import Style, RenderType


# Helper render functions that simply return a string representation
def dummy_eightbit_render(code: int) -> str:
    return f"8bit:{code}"


def dummy_rgb_render(r: int, g: int, b: int) -> str:
    return f"rgb:{r},{g},{b}"


class DummyRenderType(RenderType):
    """A minimal RenderType subclass for testing purposes."""
    pass


def test_register_call_behavior(tmp_path):
    reg = Register()
    # Register dummy render functions
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)
    reg.set_rgb_call(DummyRenderType)

    # 8bit call
    assert reg(42) == "8bit:42"

    # 24bit call
    assert reg(10, 20, 30) == "rgb:10,20,30"

    # Attribute lookup
    reg.foo = "bar"
    assert reg("foo") == "bar"

    # No-op for unsupported arg count
    assert reg() == ""
    assert reg(1, 2) == ""


def test_register_mute_and_unmute(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    # Set a style attribute
    reg.red = Style("red")
    # Muted: attribute should be rendered without value
    reg.mute()
    assert isinstance(reg.red, Style)
    assert reg.red.value == ""

    # Unmuted: attribute should restore original rendering
    reg.unmute()
    assert isinstance(reg.red, Style)
    assert reg.red.value == "red"


def test_register_setattr_with_style(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    # Assign a Style instance
    reg.green = Style("green")
    assert isinstance(reg.green, Style)
    assert reg.green.value == "green"

    # Mutate the register and reassign
    reg.mute()
    reg.green = Style("green")
    assert reg.green.value == ""


def test_register_as_dict_and_namedtuple(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    reg.red = Style("red")
    reg.green = Style("green")
    reg.blue = Style("blue")

    d = reg.as_dict()
    assert d == {"red": "red", "green": "green", "blue": "blue"}

    nt = reg.as_namedtuple()
    assert nt.red == "red"
    assert nt.green == "green"
    assert nt.blue == "blue"


def test_register_copy_deepcopy(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    reg.red = Style("red")
    reg_copy = reg.copy()

    # Ensure deep copy: modifying copy does not affect original
    reg_copy.red = Style("blue")
    assert reg.red.value == "red"
    assert reg_copy.red.value == "blue"


def test_register_set_renderfunc_updates_existing_styles(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    reg.red = Style("red")
    # Replace render function with one that appends '-new'
    def new_render(code: int) -> str:
        return f"8bit:{code}-new"

    reg.set_renderfunc(DummyRenderType, new_render)
    reg.set_eightbit_call(DummyRenderType)

    # Existing style should be updated to use new render function
    assert reg.red.value == "red"  # Style value remains same
    # But calling register with 8bit code uses new function
    assert reg(42) == "8bit:42-new"


def test_register_call_invalid_arguments_raises_no_error(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    # Passing a non-int to 8bit call should not raise, but return empty string
    assert reg("not-an-int") == ""

    # Passing more than 3 args should return empty string
    assert reg(1, 2, 3, 4) == ""


def test_register_as_dict_excludes_private_and_non_str(tmp_path):
    reg = Register()
    reg.set_renderfunc(DummyRenderType, dummy_eightbit_render)
    reg.set_eightbit_call(DummyRenderType)

    reg.red = Style("red")
    reg._private = "secret"
    reg.number = 123  # non-str attribute

    d = reg.as_dict()
    assert "_private" not in d
    assert "number" not in d
    assert "red" in d and d["red"] == "red"
