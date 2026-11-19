import pytest
from py_backwards.utils.helpers import VariablesGenerator

def test_generate_unique_names_and_counter_increment():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    name1 = VariablesGenerator.generate("foo")
    name2 = VariablesGenerator.generate("foo")
    name3 = VariablesGenerator.generate("bar")
    # Names should include the counter value at the time of generation
    assert name1 == "_py_backwards_foo_0"
    assert name2 == "_py_backwards_foo_1"
    assert name3 == "_py_backwards_bar_2"
    # Counter should now be 3
    assert VariablesGenerator._counter == 3

def test_generate_with_non_string_variable():
    # Reset counter
    VariablesGenerator._counter = 10
    # Passing a non-string should still produce a string representation
    name = VariablesGenerator.generate(None)
    assert name == "_py_backwards_None_10"
    # Counter increments regardless of input type
    assert VariablesGenerator._counter == 11

def test_generate_counter_overflow_behavior():
    # Simulate a large counter value close to sys.maxsize
    VariablesGenerator._counter = sys.maxsize - 1
    name1 = VariablesGenerator.generate("overflow")
    name2 = VariablesGenerator.generate("overflow")
    # The first name should use the large counter value
    assert name1 == f"_py_backwards_overflow_{sys.maxsize - 1}"
    # The second name should wrap around to sys.maxsize
    assert name2 == f"_py_backwards_overflow_{sys.maxsize}"
    # Counter should now be sys.maxsize + 1
    assert VariablesGenerator._counter == sys.maxsize + 1
