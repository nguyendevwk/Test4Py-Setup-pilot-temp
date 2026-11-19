import pytest
from tornado.options import define, options

def test_define_basic_option_registration():
    """Defining a simple option registers it in the global options dictionary."""
    option_name = "test_basic"
    default_value = 42
    define(option_name, default=default_value, type=int, help="A test option")
    # The option should now be present in the options registry
    assert option_name in options.options
    # The stored option should have the correct default value and type
    opt = options.options[option_name]
    assert opt.default == default_value
    assert opt.type is int

def test_define_multiple_and_callback_invocation(tmp_path):
    """Defining an option with multiple=True and a callback should store a list and invoke the callback."""
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
        help="An option that accepts multiple values",
    )
    opt = options.options[option_name]
    # Initially, the callback should not have been called
    assert not callback_called["called"]
    # Simulate setting the option value
    opt.value = ["a", "b", "c"]
    # The callback should now have been invoked with the new value
    assert callback_called["called"]
    assert callback_called["value"] == ["a", "b", "c"]
    # The option should store the list correctly
    assert opt.value == ["a", "b", "c"]

def test_define_duplicate_option_raises():
    """Defining an option with a name that already exists should raise a ValueError."""
    option_name = "test_duplicate"
    define(option_name, default=1, type=int, help="First definition")
    with pytest.raises(ValueError):
        define(option_name, default=2, type=int, help="Second definition")
