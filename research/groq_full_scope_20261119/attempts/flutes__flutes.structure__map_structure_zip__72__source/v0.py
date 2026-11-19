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
    # Ensure the result is a list of lists, not a flat list
    assert isinstance(result, list)
    assert all(isinstance(row, list) for row in result)

def test_map_structure_zip_with_dicts_and_namedtuples():
    from collections import namedtuple

    # Namedtuple for testing
    Point = namedtuple('Point', ['x', 'y'])
    pt1 = Point(1, 2)
    pt2 = Point(3, 4)
    pt3 = Point(5, 6)

    # Function to compute distance from origin
    def distance(p):
        return (p.x ** 2 + p.y ** 2) ** 0.5

    # Map over a list of namedtuples
    result = map_structure_zip(distance, [pt1, pt2, pt3])

    # Expected distances
    expected = (5.0, 5.0, 5.0)
    assert result == expected
    assert isinstance(result, tuple)

    # Test with dictionaries having identical keys
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'a': 10, 'b': 20}
    dict3 = {'a': 100, 'b': 200}

    def multiply_sum(a, b, c):
        return a * b * c

    result_dict = map_structure_zip(multiply_sum, [dict1, dict2, dict3])
    expected_dict = {'a': 1000, 'b': 8000}
    assert result_dict == expected_dict
    assert isinstance(result_dict, dict)

def test_map_structure_zip_raises_on_set_structure():
    # Sets are not allowed because they are unordered
    set1 = {1, 2}
    set2 = {3, 4}
    set3 = {5, 6}

    def dummy(a, b, c):
        return a + b + c

    with pytest.raises(ValueError, match="Structures cannot contain `set`"):
        map_structure_zip(dummy, [set1, set2, set3])
