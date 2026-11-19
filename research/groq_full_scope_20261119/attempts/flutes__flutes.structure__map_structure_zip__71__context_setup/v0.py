import pytest
from flutes.structure import map_structure_zip

def test_map_structure_zip_with_lists_and_dicts():
    # Function that sums two numbers
    def add(a, b):
        return a + b

    # Two nested lists
    list1 = [[1, 2], [3, 4]]
    list2 = [[10, 20], [30, 40]]
    result_lists = map_structure_zip(add, [list1, list2])
    assert result_lists == [[11, 22], [33, 44]]

    # Two nested dicts with same keys
    dict1 = {"x": [1, 2], "y": [3, 4]}
    dict2 = {"x": [10, 20], "y": [30, 40]}
    result_dicts = map_structure_zip(add, [dict1, dict2])
    assert result_dicts == {"x": [11, 22], "y": [33, 44]}

def test_map_structure_zip_with_namedtuple_and_tuple():
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])

    def mul(a, b):
        return a * b

    # Namedtuple instances
    p1 = Point(1, 2)
    p2 = Point(10, 20)
    result_namedtuple = map_structure_zip(mul, [p1, p2])
    assert result_namedtuple == Point(10, 40)

    # Regular tuples
    t1 = (1, 2, 3)
    t2 = (4, 5, 6)
    result_tuple = map_structure_zip(mul, [t1, t2])
    assert result_tuple == (4, 10, 18)

def test_map_structure_zip_with_set_raises_value_error():
    def dummy(a, b):
        return a + b

    set1 = {1, 2}
    set2 = {3, 4}
    with pytest.raises(ValueError, match="Structures cannot contain `set`"):
        map_structure_zip(dummy, [set1, set2])
