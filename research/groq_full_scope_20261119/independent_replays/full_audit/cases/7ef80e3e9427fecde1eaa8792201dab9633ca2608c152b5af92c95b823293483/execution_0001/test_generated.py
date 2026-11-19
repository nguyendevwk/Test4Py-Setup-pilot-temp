import pytest
from collections import namedtuple, OrderedDict
from flutes.structure import map_structure

def test_map_structure_basic_types():
    # Map over a simple list of integers
    result = map_structure(lambda x: x * 2, [1, 2, 3])
    assert result == [2, 4, 6]

    # Map over a nested structure: list of tuples
    nested = [(1, 2), (3, 4)]
    mapped = map_structure(lambda x: x + 1, nested)
    assert mapped == [(2, 3), (4, 5)]

    # Map over a dictionary preserving keys
    d = {"a": 1, "b": 2}
    mapped_d = map_structure(lambda x: x * 10, d)
    assert mapped_d == {"a": 10, "b": 20}

def test_map_structure_boundary_and_namedtuple():
    # Empty list should return an empty list
    assert map_structure(lambda x: x, []) == []

    # Namedtuple should preserve type and map each field
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    mapped_p = map_structure(lambda x: x * 3, p)
    assert isinstance(mapped_p, Point)
    assert mapped_p == Point(3, 6)

    # OrderedDict should preserve order
    od = OrderedDict([("first", 1), ("second", 2)])
    mapped_od = map_structure(lambda x: x + 5, od)
    assert isinstance(mapped_od, OrderedDict)
    assert list(mapped_od.items()) == [("first", 6), ("second", 7)]

def test_map_structure_error_behavior():
    # Passing a non-callable fn should raise TypeError
    with pytest.raises(TypeError):
        map_structure(None, [1, 2, 3])

    # Passing a non-collection obj should still apply fn
    # Here we use a string; it is not a collection in the sense of the function
    result = map_structure(lambda x: x.upper(), "abc")
    assert result == "ABC"

    # Passing a set should return a set of mapped values
    s = {1, 2, 3}
    mapped_s = map_structure(lambda x: x * x, s)
    assert mapped_s == {1, 4, 9}
