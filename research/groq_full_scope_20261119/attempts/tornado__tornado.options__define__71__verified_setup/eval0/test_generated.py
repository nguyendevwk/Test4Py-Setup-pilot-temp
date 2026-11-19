import pytest
import tornado.options as options
from tornado.options import define

def test_define_basic(tmp_path):
    # Define a simple option and verify it is stored correctly
    option_name = "test_basic"
    default_value = 42
    define(option_name, default=default_value, type=int, help="basic test")
    # The option should now be present in the global options registry
    opt = options.options.get(option_name)
    assert opt is not None, f"Option {option_name} not found after definition"
    assert opt.default == default_value
    assert opt.type is int
    assert opt.help == "basic test"
    # Clean up for isolation
    options.options.pop(option_name, None)

def test_define_multiple_with_callback(tmp_path):
    # Define an option that accepts multiple values and uses a callback
    option_name = "test_multiple"
    callback_called = {"called": False, "value": None}

    def callback(value):
        callback_called["called"] = True
        callback_called["value"] = value

    define(
        option_name,
        default=[],
        type=str,
        multiple=True,
        callback=callback,
        help="multiple values test",
    )
    opt = options.options.get(option_name)
    assert opt is not None
    assert opt.multiple is True
    # Simulate setting the option to trigger the callback
    opt.set(["a", "b", "c"])
    assert callback_called["called"] is True
    assert callback_called["value"] == ["a", "b", "c"]
    # Clean up
    options.options.pop(option_name, None)

def test_define_invalid_type_raises(tmp_path):
    # Passing an invalid type should raise a TypeError during definition
    with pytest.raises(TypeError):
        define("invalid_type", default="foo", type="not_a_type")
