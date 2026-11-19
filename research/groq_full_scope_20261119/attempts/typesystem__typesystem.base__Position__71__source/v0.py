import pytest
from typesystem.base import Position


def test_position_equality_and_repr():
    """Verify that Position objects compare equal when all fields match
    and that __repr__ returns the expected string format."""
    p1 = Position(1, 5, 10)
    p2 = Position(1, 5, 10)
    p3 = Position(2, 5, 10)

    # Equality
    assert p1 == p2
    assert not (p1 == p3)

    # Representation
    expected_repr = "Position(line_no=1, column_no=5, char_index=10)"
    assert repr(p1) == expected_repr
    assert repr(p3) == "Position(line_no=2, column_no=5, char_index=10)"


def test_position_comparison_with_non_position():
    """Ensure that Position objects are not considered equal to objects of other types."""
    p = Position(3, 7, 15)
    assert p != 42
    assert p != "Position(3, 7, 15)"
    assert p != {"line_no": 3, "column_no": 7, "char_index": 15}


def test_position_boundary_values():
    """Test Position with extreme integer values to confirm no overflow or type errors."""
    max_int = 2**63 - 1
    min_int = -2**63

    p_max = Position(max_int, max_int, max_int)
    p_min = Position(min_int, min_int, min_int)

    # Equality with self
    assert p_max == Position(max_int, max_int, max_int)
    assert p_min == Position(min_int, min_int, min_int)

    # Representation includes the large numbers correctly
    assert "line_no=9223372036854775807" in repr(p_max)
    assert "line_no=-9223372036854775808" in repr(p_min)
