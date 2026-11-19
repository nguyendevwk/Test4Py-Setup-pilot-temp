import sys
import types
import pytest

# Provide a minimal stub for the external `six` dependency used by genty.
six_stub = types.SimpleNamespace()
six_stub.string_types = (str,)
sys.modules["six"] = six_stub

# Import the target decorator after the stub is in place.
from genty.genty_repeat import genty_repeat


def test_genty_repeat_decorator_sets_count_and_raises_for_negative():
    # Positive count: decorator should attach the count and return the same function
    count = 5
    decorator = genty_repeat(count)

    def dummy_test(self):
        pass

    wrapped = decorator(dummy_test)
    assert wrapped is dummy_test
    assert getattr(wrapped, "genty_repeat_count") == count

    # Zero count: still valid and should set attribute to 0
    zero_decorator = genty_repeat(0)
    wrapped_zero = zero_decorator(dummy_test)
    assert getattr(wrapped_zero, "genty_repeat_count") == 0

    # Negative count: should raise ValueError with informative message
    with pytest.raises(ValueError) as excinfo:
        genty_repeat(-1)
    assert "Can't have -1 iterations" in str(excinfo.value)
