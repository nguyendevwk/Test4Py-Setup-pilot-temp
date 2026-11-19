import pytest
from py_backwards.utils.helpers import VariablesGenerator

def test_generate_unique_names_and_counter_increment():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    name1 = VariablesGenerator.generate("foo")
    name2 = VariablesGenerator.generate("foo")
    name3 = VariablesGenerator.generate("bar")
    # Names should contain the variable part and a unique counter
    assert name1 == "_py_backwards_foo_0"
    assert name2 == "_py_backwards_foo_1"
    assert name3 == "_py_backwards_bar_2"
    # Counter should have incremented to 3
    assert VariablesGenerator._counter == 3

def test_generate_with_non_string_input():
    # Reset counter
    VariablesGenerator._counter = 10
    # Passing an integer should be converted to string
    name = VariablesGenerator.generate(42)
    assert name == "_py_backwards_42_10"
    # Counter increments after generation
    assert VariablesGenerator._counter == 11

def test_generate_counter_persistence_across_instances():
    # Reset counter
    VariablesGenerator._counter = 0
    # Generate names using two different class references
    name_a = VariablesGenerator.generate("a")
    name_b = VariablesGenerator.generate("b")
    # Counter should be shared across class references
    assert name_a == "_py_backwards_a_0"
    assert name_b == "_py_backwards_b_1"
    assert VariablesGenerator._counter == 2
