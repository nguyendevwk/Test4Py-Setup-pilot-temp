import pytest
import types
from pysnooper import variables

# Minimal concrete implementation of BaseVariable for testing
class DummyVariable(variables.BaseVariable):
    def _items(self, key, normalize=False):
        # Return a single item tuple for demonstration
        return ((key, key),)

def test_items_success(tmp_path):
    # Create a dummy variable that evaluates to a string
    var = DummyVariable("'hello world'")
    # Build a frame with globals and locals that the eval will use
    frame = types.FrameType(
        None, None, None, None, {}, {}, None, None, None, None, None, None, None
    )
    # The eval should succeed and return the string
    result = var.items(frame)
    assert result == (("hello world", "hello world"),)

def test_items_exception():
    # Source that raises ZeroDivisionError when evaluated
    var = DummyVariable("1/0")
    frame = types.FrameType(
        None, None, None, None, {}, {}, None, None, None, None, None, None, None
    )
    # items should return an empty tuple on exception
    assert var.items(frame) == ()

def test_equality_and_hash():
    var1 = DummyVariable("x", exclude=('y',))
    var2 = DummyVariable("x", exclude=('y',))
    var3 = DummyVariable("x", exclude=('z',))
    # Equality based on fingerprint
    assert var1 == var2
    assert var1 != var3
    # Hash consistency
    assert hash(var1) == hash(var2)
    assert hash(var1) != hash(var3)
