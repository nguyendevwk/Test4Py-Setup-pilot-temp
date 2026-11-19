import pytest
from typesystem.base import Position


def test_position_equality_and_repr():
    """Verify that two Position instances with identical values are equal
    and that the __repr__ output matches the expected format."""
    p1 = Position(10, 5, 50)
    p2 = Position(10, 5, 50)
    p3 = Position(1, 1, 1)

    # Equality
    assert p1 == p2
    assert not (p1 == p3)

    # __repr__ format
    expected_repr = "Position(line_no=10, column_no=5, char_index=50)"
    assert repr(p1) == expected_repr


def test_position_comparison_with_non_position():
    """Ensure that Position instances are not considered equal to objects
    of other types, even if they have similar attributes."""
    p = Position(2, 3, 4)
    class Dummy:
        def __init__(self):
            self.line_no = 2
            self.column_no = 3
            self.char_index = 4

    dummy = Dummy()
    assert p != dummy
    assert not (p == dummy)


def test_position_boundary_values():
    """Test Position with extreme integer values to confirm no overflow
    or unexpected behavior occurs."""
    import sys

    max_int = sys.maxsize
    min_int = -sys.maxsize - 1

    p_max = Position(max_int, max_int, max_int)
    p_min = Position(min_int, min_int, min_int)

    # Equality with self
    assert p_max == Position(max_int, max_int, max_int)
    assert p_min == Position(min_int, min_int, min_int)

    # Representation contains the extreme values
    assert f"line_no={max_int}" in repr(p_max)
    assert f"column_no={min_int}" in repr(p_min)
