import pytest
from tornado import options

def test_define_basic_option(tmp_path):
    # Define a simple option and verify it is stored correctly
    options.define("test_option", default=42, type=int, help="A test integer")
    # The option should be accessible via options.options dict
    opt = options.options.get("test_option")
    assert opt is not None
    assert opt.default == 42
    assert opt.type is int
    assert opt.help == "A test integer"
    # Clean up for other tests
    del options.options["test_option"]

def test_define_multiple_option(tmp_path):
    # Define an option that accepts multiple values
    options.define("multi_option", default=[], type=str, multiple=True)
    opt = options.options.get("multi_option")
    assert opt is not None
    assert opt.multiple is True
    # The default should be an empty list
    assert opt.default == []
    # Clean up
    del options.options["multi_option"]

def test_define_duplicate_name_raises(tmp_path):
    # Define an option and then attempt to define it again
    options.define("dup_option", default="first")
    with pytest.raises(ValueError):
        options.define("dup_option", default="second")
    # Clean up
    del options.options["dup_option"]
