import pytest
from py_backwards.utils.helpers import VariablesGenerator

def test_generate_basic_unique_names():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    name1 = VariablesGenerator.generate("foo")
    name2 = VariablesGenerator.generate("foo")
    name3 = VariablesGenerator.generate("bar")
    # Names should include the variable part and a unique counter suffix
    assert name1 == "_py_backwards_foo_0"
    assert name2 == "_py_backwards_foo_1"
    assert name3 == "_py_backwards_bar_2"
    # Ensure counter increments correctly
    assert VariablesGenerator._counter == 3

def test_generate_counter_increments_across_calls():
    # Start from a known counter value
    VariablesGenerator._counter = 10
    name = VariablesGenerator.generate("test")
    assert name == "_py_backwards_test_10"
    # Counter should have incremented by one
    assert VariablesGenerator._counter == 11
    # Subsequent call should use the new counter value
    name2 = VariablesGenerator.generate("test")
    assert name2 == "_py_backwards_test_11"
    assert VariablesGenerator._counter == 12

def test_generate_with_non_string_input_raises_type_error():
    # The function expects a string; passing a non-string should raise a TypeError
    with pytest.raises(TypeError):
        VariablesGenerator.generate(123)  # type: ignore[arg-type]
