import pytest
from typesystem.base import Position


def test_position_equality_and_repr():
    """Verify that Position objects compare equal when all attributes match
    and that the representation string contains the correct values."""
    pos1 = Position(1, 5, 10)
    pos2 = Position(1, 5, 10)
    pos3 = Position(2, 5, 10)

    # Equality
    assert pos1 == pos2
    assert not (pos1 == pos3)

    # Representation
    expected_repr = "Position(line_no=1, column_no=5, char_index=10)"
    assert repr(pos1) == expected_repr
    assert repr(pos3) == "Position(line_no=2, column_no=5, char_index=10)"


def test_position_comparison_with_non_position():
    """Ensure that Position objects are not considered equal to objects of other types."""
    pos = Position(3, 7, 15)
    assert pos != 42
    assert pos != (3, 7, 15)
    assert pos != {"line_no": 3, "column_no": 7, "char_index": 15}


def test_position_boundary_values():
    """Test Position with extreme integer values to confirm no overflow or type errors."""
    max_int = 2**63 - 1
    min_int = -2**63

    pos_max = Position(max_int, max_int, max_int)
    pos_min = Position(min_int, min_int, min_int)

    # Equality with identical extreme values
    assert pos_max == Position(max_int, max_int, max_int)
    assert pos_min == Position(min_int, min_int, min_int)

    # Representation includes the extreme values
    assert repr(pos_max) == f"Position(line_no={max_int}, column_no={max_int}, char_index={max_int})"
    assert repr(pos_min) == f"Position(line_no={min_int}, column_no={min_int}, char_index={min_int})"
