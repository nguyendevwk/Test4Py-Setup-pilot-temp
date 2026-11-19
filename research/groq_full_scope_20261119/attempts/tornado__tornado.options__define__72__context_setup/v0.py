import os
import pytest
from tornado.options import define, options


def test_define_basic_and_default(tmp_path):
    """Define a simple option and verify default value and help text."""
    # Ensure the option name is unique for this test
    opt_name = "test_basic_option"
    # Remove any existing option with the same name
    if opt_name in options._options:
        del options._options[opt_name]

    define(
        name=opt_name,
        default="hello",
        help="A simple test option",
        metavar="VALUE",
    )

    # The option should be registered in the global options
    assert opt_name in options._options
    opt = options._options[opt_name]
    assert opt.default == "hello"
    assert opt.help == "A simple test option"
    assert opt.metavar == "VALUE"

    # The current value should be the default initially
    assert options[opt_name] == "hello"

    # Change the value and verify the change
    options[opt_name] = "world"
    assert options[opt_name] == "world"


def test_define_type_error(tmp_path):
    """Defining an option with a type and passing an invalid value should raise."""
    opt_name = "test_type_option"
    if opt_name in options._options:
        del options._options[opt_name]

    define(
        name=opt_name,
        default=10,
        type=int,
        help="An integer option",
    )

    # Setting a valid integer should work
    options[opt_name] = 42
    assert options[opt_name] == 42

    # Setting a non-integer should raise a ValueError
    with pytest.raises(ValueError):
        options[opt_name] = "not an int"


def test_define_multiple_and_callback(tmp_path):
    """Define an option that accepts multiple values and triggers a callback."""
    opt_name = "test_multiple_option"
    if opt_name in options._options:
        del options._options[opt_name]

    # Path for the callback to write to
    callback_file = tmp_path / "callback.txt"

    def write_to_file(value):
        # The callback receives the final value (a list)
        with open(callback_file, "w") as f:
            f.write(",".join(map(str, value)))

    define(
        name=opt_name,
        default=[],
        type=str,
        multiple=True,
        callback=write_to_file,
        help="An option that accepts multiple string values",
    )

    # Assign multiple values
    options[opt_name] = ["a", "b", "c"]
    assert options[opt_name] == ["a", "b", "c"]

    # The callback should have written the values to the file
    assert callback_file.exists()
    content = callback_file.read_text()
    assert content == "a,b,c"
