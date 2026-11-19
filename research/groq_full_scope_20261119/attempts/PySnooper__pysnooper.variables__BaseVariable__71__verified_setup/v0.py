import builtins
import types
import pytest
from pysnooper.variables import BaseVariable

# A minimal concrete implementation of BaseVariable for testing purposes.
class SimpleVariable(BaseVariable):
    def _items(self, key, normalize=False):
        # For testing, simply return the key wrapped in a tuple.
        return [(None, key)]


def test_items_normal_evaluation(tmp_path):
    """Test that items returns the expected value when evaluation succeeds."""
    # Prepare a frame with a local variable `x`.
    frame = types.FrameType(
        None, {}, {"x": 42}, None, None, None, None, None, None, None, None, None
    )
    var = SimpleVariable("x")
    result = var.items(frame)
    assert result == [(None, 42)], "Expected the evaluated value to be returned in a tuple."


def test_items_evaluation_exception(tmp_path):
    """Test that items returns an empty tuple when evaluation raises an exception."""
    # Prepare a frame without the variable `y` to trigger a NameError.
    frame = types.FrameType(
        None, {}, {}, None, None, None, None, None, None, None, None, None
    )
    var = SimpleVariable("y")
    result = var.items(frame)
    assert result == (), "Expected an empty tuple when evaluation fails."


def test_fingerprint_equality_and_hash(tmp_path):
    """Test that two variables with the same source and exclude are equal and hash to the same value."""
    var1 = SimpleVariable("x", exclude=("y",))
    var2 = SimpleVariable("x", exclude=("y",))
    var3 = SimpleVariable("x", exclude=("z",))
    assert var1 == var2, "Variables with identical source and exclude should be equal."
    assert hash(var1) == hash(var2), "Hashes of equal variables should match."
    assert var1 != var3, "Variables with different exclude should not be equal."
