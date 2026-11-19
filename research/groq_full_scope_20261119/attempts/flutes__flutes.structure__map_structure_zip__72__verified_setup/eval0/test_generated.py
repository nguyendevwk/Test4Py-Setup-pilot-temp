import pytest
from flutes.structure import map_structure_zip

def test_map_structure_zip_with_lists_and_nested_lists():
    # Function to sum three numbers
    def add(a, b, c):
        return a + b + c

    # Two nested lists with identical structure
    list1 = [[1, 2], [3, 4]]
    list2 = [[10, 20], [30, 40]]
    list3 = [[100, 200], [300, 400]]

    result = map_structure_zip(add, [list1, list2, list3])

    # Expected structure: same nested lists, each element is the sum
    expected = [[111, 222], [333, 444]]
    assert result == expected

def test_map_structure_zip_with_dicts_and_namedtuples():
    from collections import namedtuple

    # Function to concatenate string representations
    def concat(a, b, c):
        return f"{a}-{b}-{c}"

    # Two dictionaries with identical keys and values that are namedtuples
    Point = namedtuple("Point", ["x", "y"])
    dict1 = {"p1": Point(1, 2), "p2": Point(3, 4)}
    dict2 = {"p1": Point(10, 20), "p2": Point(30, 40)}
    dict3 = {"p1": Point(100, 200), "p2": Point(300, 400)}

    result = map_structure_zip(concat, [dict1, dict2, dict3])

    # Expected dictionary with namedtuple values concatenated
    expected = {
        "p1": "1-10-100",
        "p2": "3-30-300",
    }
    assert result == expected

def test_map_structure_zip_raises_on_set_structure():
    # Function to multiply three numbers
    def mul(a, b, c):
        return a * b * c

    # Set is unordered; should raise ValueError
    set1 = {1, 2}
    set2 = {10, 20}
    set3 = {100, 200}

    with pytest.raises(ValueError, match="Structures cannot contain `set`"):
        map_structure_zip(mul, [set1, set2, set3])
