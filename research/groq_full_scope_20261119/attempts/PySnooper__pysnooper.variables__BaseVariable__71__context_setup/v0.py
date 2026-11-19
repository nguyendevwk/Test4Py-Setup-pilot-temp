import types
import pytest
from pysnooper.variables import BaseVariable, needs_parentheses


class DummyVar(BaseVariable):
    """Concrete implementation of BaseVariable for testing."""

    def _items(self, key, normalize=False):
        # Return a simple list containing the key twice for visibility.
        return [(key, key)]


def test_items_evaluates_and_returns_correct_tuple():
    """Test that items evaluates the source and returns the expected tuple."""
    # Prepare a frame with a local variable `x`.
    local_vars = {"x": 42}
    frame = types.FrameType(
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    # Monkey‑patch the frame's locals and globals.
    frame.f_locals = local_vars
    frame.f_globals = {}

    var = DummyVar("x")
    result = var.items(frame)
    assert result == [(42, 42)], "items should return a tuple with the evaluated value"


def test_unambiguous_source_and_needs_parentheses():
    """Test that unambiguous_source is set correctly based on needs_parentheses."""
    # Source that does not need parentheses.
    var_simple = DummyVar("x")
    assert var_simple.unambiguous_source == "x"
    assert not needs_parentheses("x")

    # Source that does need parentheses.
    var_attr = DummyVar("x.y")
    assert var_attr.unambiguous_source == "(x.y)"
    assert needs_parentheses("x.y")


def test_items_handles_evaluation_error_and_exclude():
    """Test that items returns an empty tuple on eval error and exclude is stored."""
    # Source that will raise ZeroDivisionError when evaluated.
    var_error = DummyVar("1/0", exclude=("x",))
    # Create a dummy frame; the eval will raise, so items should return empty tuple.
    frame = types.FrameType(
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
    )
    frame.f_locals = {}
    frame.f_globals = {}

    assert var_error.items(frame) == (), "items should return empty tuple on eval error"
    # Verify that exclude was stored as a tuple.
    assert var_error.exclude == ("x",), "exclude should be stored as a tuple"
