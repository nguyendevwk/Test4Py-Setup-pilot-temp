import pytest
from typesystem.base import Position


def test_position_equality_and_repr():
    """Normal construction and equality comparison."""
    p1 = Position(1, 5, 10)
    p2 = Position(1, 5, 10)
    p3 = Position(2, 3, 7)

    # Equality
    assert p1 == p2
    assert p1 != p3

    # Representation
    expected_repr = "Position(line_no=1, column_no=5, char_index=10)"
    assert repr(p1) == expected_repr


def test_position_comparison_with_non_position():
    """Equality comparison with non-Position objects."""
    p = Position(0, 0, 0)
    assert p != 42
    assert p != "Position(0, 0, 0)"
    assert p != None
    assert p != (0, 0, 0)


def test_position_boundary_values():
    """Boundary values for line_no, column_no, and char_index."""
    # Minimum integer values
    p_min = Position(-1, -1, -1)
    assert p_min.line_no == -1
    assert p_min.column_no == -1
    assert p_min.char_index == -1

    # Large integer values
    large = 10**12
    p_large = Position(large, large, large)
    assert p_large.line_no == large
    assert p_large.column_no == large
    assert p_large.char_index == large
