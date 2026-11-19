import pytest
from py_backwards.utils.helpers import VariablesGenerator

def test_generate_increments_counter(tmp_path):
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    first = VariablesGenerator.generate("foo")
    second = VariablesGenerator.generate("foo")
    third = VariablesGenerator.generate("bar")
    # Ensure counter increments and names are unique
    assert first == "_py_backwards_foo_0"
    assert second == "_py_backwards_foo_1"
    assert third == "_py_backwards_bar_2"
    # Counter should now be 3
    assert VariablesGenerator._counter == 3

def test_generate_with_empty_and_special_chars():
    # Reset counter
    VariablesGenerator._counter = 0
    empty = VariablesGenerator.generate("")
    special = VariablesGenerator.generate("!@#$")
    # Names should contain the variable string and counter
    assert empty == "_py_backwards__0"
    assert special == "_py_backwards_!@#$1"
    # Counter should be 2 after two calls
    assert VariablesGenerator._counter == 2

def test_generate_with_non_string_input():
    # Reset counter
    VariablesGenerator._counter = 0
    # Passing an integer should be converted to string
    int_name = VariablesGenerator.generate(42)
    # Passing a list should be converted to string representation
    list_name = VariablesGenerator.generate([1, 2])
    assert int_name == "_py_backwards_42_0"
    assert list_name == "_py_backwards_[1, 2]_1"
    # Counter should be 2 after two calls
    assert VariablesGenerator._counter == 2
