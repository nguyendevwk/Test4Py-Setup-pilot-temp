import pytest
from pymonet.box import Box

def test_box_map_and_equality():
    """Test that map applies a function and equality works."""
    b = Box(10)
    mapped = b.map(lambda x: x * 2)
    assert isinstance(mapped, Box)
    assert mapped.value == 20
    assert mapped == Box(20)
    assert b != mapped  # different values

def test_box_bind_returns_raw_value():
    """Test that bind returns the raw result of the mapper."""
    b = Box("hello")
    result = b.bind(lambda s: s.upper())
    assert result == "HELLO"
    assert isinstance(result, str)

def test_box_ap_applies_function_from_other_box():
    """Test that ap applies the function inside the Box to another Box."""
    func_box = Box(lambda x: x + 5)
    value_box = Box(7)
    applied = value_box.ap(func_box)
    assert isinstance(applied, Box)
    assert applied.value == 12
    assert applied == Box(12)
