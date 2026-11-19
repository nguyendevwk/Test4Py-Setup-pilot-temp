import pytest
from tornado import options

def test_define_registers_option_and_callback(tmp_path):
    # Define a simple option with a callback that records when it's called
    called = {"flag": False}

    def _cb(value):
        called["flag"] = True
        # Ensure the value passed to callback is the default
        assert value == 42

    options.define(
        name="test_option",
        default=42,
        type=int,
        help="A test option",
        callback=_cb,
    )

    # The option should now be registered in the global options registry
    assert "test_option" in options.options
    opt = options.options["test_option"]
    assert opt.default == 42
    assert opt.type is int

    # Setting the option's value should trigger the callback
    opt.value = 42
    assert called["flag"] is True

def test_define_multiple_option_accepts_list(tmp_path):
    # Define an option that accepts multiple values
    options.define(
        name="multi_opt",
        default=[],
        type=int,
        multiple=True,
        help="An option that accepts multiple values",
    )

    opt = options.options["multi_opt"]
    # The default should be an empty list
    assert opt.default == []

    # Assign a list of integers
    opt.value = [1, 2, 3]
    assert opt.value == [1, 2, 3]
    # The type should still be int for each element
    for v in opt.value:
        assert isinstance(v, int)

def test_define_invalid_callback_raises_type_error(tmp_path):
    # Passing a non-callable as callback should raise a TypeError
    with pytest.raises(TypeError):
        options.define(
            name="bad_cb",
            default="foo",
            callback="not_a_function",
        )
