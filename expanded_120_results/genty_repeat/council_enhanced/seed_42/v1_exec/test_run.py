import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_behavior():
    # Positive count: decorator should set attribute and return the same function
    def dummy(self): pass
    count = 3
    decorator = genty_repeat(count)
    decorated = decorator(dummy)
    assert decorated is dummy
    assert getattr(decorated, "genty_repeat_count") == count

    # Zero count: still valid, attribute set to 0
    zero_decorator = genty_repeat(0)
    zero_decorated = zero_decorator(dummy)
    assert zero_decorated is dummy
    assert zero_decorated.genty_repeat_count == 0

    # Negative count: should raise ValueError
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-1)
    assert "Can't have -1 iterations" in str(excinfo.value)
