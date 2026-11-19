import pytest
from pymonet.box import Box

def test_box_equality_and_str():
    """Box equality should compare stored values and __str__ should reflect value."""
    a = Box(10)
    b = Box(10)
    c = Box(20)
    assert a == b
    assert a != c
    # __str__ is not covered by coverage but should produce a readable representation
    assert str(a) == "Box[value=10]"

def test_box_map_transforms_value():
    """map should apply a function to the stored value and return a new Box."""
    original = Box(5)
    doubled = original.map(lambda x: x * 2)
    assert isinstance(doubled, Box)
    assert doubled.value == 10
    # original should remain unchanged
    assert original.value == 5

def test_box_bind_and_ap_behaviour():
    """bind should apply a function and return its result; ap should apply the Box's value as a function."""
    # bind example
    box = Box(3)
    result = box.bind(lambda x: x + 7)
    assert result == 10

    # ap example: Box containing a function applied to another Box
    func_box = Box(lambda x: x * 4)
    value_box = Box(2)
    applied = value_box.ap(func_box)
    assert isinstance(applied, Box)
    assert applied.value == 8
