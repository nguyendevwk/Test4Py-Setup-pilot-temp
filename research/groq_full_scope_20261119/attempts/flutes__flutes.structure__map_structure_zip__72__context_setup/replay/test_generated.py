import pytest
from flutes.structure import map_structure_zip

def test_map_structure_zip_with_lists_and_nested():
    # Function that sums three numbers
    def add(a, b, c):
        return a + b + c

    # Two nested lists with identical structure
    list1 = [[1, 2], [3, 4]]
    list2 = [[10, 20], [30, 40]]
    list3 = [[100, 200], [300, 400]]

    result = map_structure_zip(add, [list1, list2, list3])

    # Expected sums at each position
    expected = [[111, 222], [333, 444]]
    assert result == expected, f"Expected {expected}, got {result}"

def test_map_structure_zip_with_dicts_and_namedtuple():
    from collections import namedtuple

    # Function that concatenates string representations
    def concat(a, b, c):
        return f"{a}-{b}-{c}"

    # Two dictionaries with identical keys and nested namedtuples
    Point = namedtuple("Point", ["x", "y"])
    dict1 = {"p1": Point(1, 2), "p2": Point(3, 4)}
    dict2 = {"p1": Point(10, 20), "p2": Point(30, 40)}
    dict3 = {"p1": Point(100, 200), "p2": Point(300, 400)}

    result = map_structure_zip(concat, [dict1, dict2, dict3])

    # Expected concatenated strings for each namedtuple
    expected = {
        "p1": Point("1-10-100", "2-20-200"),
        "p2": Point("3-30-300", "4-40-400"),
    }
    assert result == expected, f"Expected {expected}, got {result}"

def test_map_structure_zip_with_set_raises_value_error():
    # Function that would normally work
    def dummy(a, b):
        return a + b

    # Two sets with identical elements
    set1 = {1, 2}
    set2 = {10, 20}

    with pytest.raises(ValueError, match="Structures cannot contain `set`"):
        map_structure_zip(dummy, [set1, set2])
