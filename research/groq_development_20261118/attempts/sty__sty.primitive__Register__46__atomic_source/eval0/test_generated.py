import pytest
from sty.primitive import Register
from sty.rendertype import RenderType


class DummyRenderType(RenderType):
    """Simple RenderType that returns a formatted string for testing."""
    def __call__(self, *args, **kwargs):
        return f"DUMMY:{args}:{kwargs}"


def test_register_call_and_renderfuncs(tmp_path):
    reg = Register()
    # Register a dummy render function for DummyRenderType
    reg.set_renderfunc(DummyRenderType, DummyRenderType())
    # Set the eightbit and rgb call to use DummyRenderType
    reg.set_eightbit_call(DummyRenderType)
    reg.set_rgb_call(DummyRenderType)

    # Test 8-bit call
    result_8bit = reg(42)
    assert result_8bit == "DUMMY:(42,):{}"

    # Test 24-bit call
    result_rgb = reg(10, 20, 30)
    assert result_rgb == "DUMMY:(10, 20, 30,):{}"

    # Test attribute access via string
    reg.foo = "bar"
    assert reg("foo") == "bar"


def test_register_mute_and_unmute(tmp_path):
    reg = Register()
    reg.foo = "bar"
    # Muting should replace style attributes with empty strings
    reg.mute()
    assert reg.foo == ""
    # Unmuting restores original value
    reg.unmute()
    assert reg.foo == "bar"


def test_register_as_dict_and_namedtuple(tmp_path):
    reg = Register()
    reg.red = "red_value"
    reg.green = "green_value"
    # as_dict should include only non-private string attributes
    d = reg.as_dict()
    assert d == {"red": "red_value", "green": "green_value"}
    # as_namedtuple should produce a namedtuple with the same values
    nt = reg.as_namedtuple()
    assert nt.red == "red_value"
    assert nt.green == "green_value"
