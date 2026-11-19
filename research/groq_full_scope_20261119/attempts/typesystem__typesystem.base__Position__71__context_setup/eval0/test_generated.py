import re
import pytest
from typesystem.base import Position


def test_position_equality_and_repr():
    """Verify that two Position objects with identical data are equal and that
    the __repr__ output contains the correct field values."""
    p1 = Position(1, 5, 10)
    p2 = Position(1, 5, 10)
    assert p1 == p2
    assert isinstance(p1, Position)
    # __repr__ should include class name and all fields
    rep = repr(p1)
    assert rep.startswith("Position(")
    assert "line_no=1" in rep
    assert "column_no=5" in rep
    assert "char_index=10" in rep
    # The representation should be a valid Python expression that could be eval'd
    # (ignoring the class import context)
    pattern = r"Position\(line_no=1, column_no=5, char_index=10\)"
    assert re.fullmatch(pattern, rep)


def test_position_inequality_with_different_values():
    """Positions with any differing field should not be equal."""
    base = Position(2, 3, 4)
    # Change each field one at a time
    diff_line = Position(5, 3, 4)
    diff_column = Position(2, 7, 4)
    diff_char = Position(2, 3, 9)
    assert base != diff_line
    assert base != diff_column
    assert base != diff_char
    # Ensure that equality is symmetric
    assert not (diff_line == base)
    assert not (diff_column == base)
    assert not (diff_char == base)


def test_position_comparison_with_non_position():
    """Comparing a Position to an object of a different type should return False."""
    p = Position(0, 0, 0)
    assert p != 42
    assert p != "Position(0, 0, 0)"
    assert p != None
    assert p != [0, 0, 0]
    # Ensure that __eq__ does not raise an exception for any arbitrary object
    class Dummy:  # noqa: D401
        pass
    dummy = Dummy()
    assert p != dummy
