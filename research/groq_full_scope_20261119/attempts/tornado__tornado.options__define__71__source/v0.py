import pytest
import os
import tempfile
from tornado import options

# Test 1: Normal option definition and retrieval
def test_define_and_get_option(tmp_path):
    # Define a simple string option
    options.define("test_option", default="hello", type=str, help="A test option")
    # Retrieve the option value
    assert options.options.test_option == "hello"
    # Change the value via the options namespace
    options.options.test_option = "world"
    assert options.options.test_option == "world"
    # Ensure the option is registered in the options registry
    assert "test_option" in options.options._options

# Test 2: Multiple values option handling
def test_define_multiple_option(tmp_path):
    # Define an option that accepts multiple values
    options.define("multi_option", default=[], type=int, multiple=True, help="Multiple ints")
    # Set multiple values
    options.options.multi_option = [1, 2, 3]
    assert options.options.multi_option == [1, 2, 3]
    # Append a new value
    options.options.multi_option.append(4)
    assert options.options.multi_option == [1, 2, 3, 4]
    # Ensure the option type enforcement works
    with pytest.raises(TypeError):
        options.options.multi_option.append("not an int")

# Test 3: Error handling for invalid type specification
def test_define_invalid_type(tmp_path):
    # Attempt to define an option with an unsupported type (e.g., a set)
    with pytest.raises(TypeError):
        options.define("bad_option", default=set(), type=set, help="Unsupported type")
