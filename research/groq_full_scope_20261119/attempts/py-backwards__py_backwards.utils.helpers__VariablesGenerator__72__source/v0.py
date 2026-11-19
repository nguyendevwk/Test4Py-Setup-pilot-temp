import pytest
from py_backwards.utils.helpers import VariablesGenerator

def test_generate_increments_counter_and_includes_variable():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    first = VariablesGenerator.generate("foo")
    second = VariablesGenerator.generate("foo")
    third = VariablesGenerator.generate("bar")

    assert first == "_py_backwards_foo_0"
    assert second == "_py_backwards_foo_1"
    assert third == "_py_backwards_bar_2"
    # Ensure counter has been incremented correctly
    assert VariablesGenerator._counter == 3

def test_generate_with_non_string_input_converts_to_string():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    result = VariablesGenerator.generate(42)
    assert result == "_py_backwards_42_0"
    # Counter should have incremented
    assert VariablesGenerator._counter == 1

def test_generate_raises_type_error_on_none_input():
    # Reset counter for deterministic test
    VariablesGenerator._counter = 0
    with pytest.raises(TypeError):
        VariablesGenerator.generate(None)
