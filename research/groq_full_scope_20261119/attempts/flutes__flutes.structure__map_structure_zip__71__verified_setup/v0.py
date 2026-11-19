import pytest
from flutes.structure import map_structure_zip

def test_map_structure_zip_with_lists_and_dicts():
    # Normal case: nested lists and dicts with identical structure
    data = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    result = map_structure_zip(lambda *x: sum(x), data)
    assert result == [12, 15, 18]  # 1+4+7, 2+5+8, 3+6+9

    # Nested dicts
    nested = [
        {'a': [1, 2], 'b': [3, 4]},
        {'a': [5, 6], 'b': [7, 8]}
    ]
    result = map_structure_zip(lambda *x: sum(x), nested)
    assert result == {'a': [6, 8], 'b': [10, 12]}

def test_map_structure_zip_with_namedtuple_and_tuple():
    from collections import namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    objs = [
        Point(1, 2),
        Point(3, 4),
        Point(5, 6)
    ]
    # Function that returns a new Point with summed coordinates
    def sum_points(p1, p2, p3):
        return Point(p1.x + p2.x + p3.x, p1.y + p2.y + p3.y)
    result = map_structure_zip(sum_points, objs)
    assert result == Point(9, 12)

def test_map_structure_zip_with_set_raises_value_error():
    # Sets are not allowed because they are unordered
    data = [
        {1, 2},
        {3, 4}
    ]
    with pytest.raises(ValueError, match="Structures cannot contain `set`"):
        map_structure_zip(lambda *x: sum(x), data)
