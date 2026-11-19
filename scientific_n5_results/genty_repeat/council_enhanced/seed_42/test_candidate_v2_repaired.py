import sys
import types
import pytest

# Provide a minimal stub for the `six` module required by genty
six_stub = types.SimpleNamespace(
    string_types=(str, bytes),
    text_type=str,
    binary_type=bytes,
    iteritems=lambda d: d.items(),
    iterkeys=lambda d: d.keys(),
    itervalues=lambda d: d.values(),
)
sys.modules["six"] = six_stub

from genty.genty_repeat import genty_repeat


def test_genty_repeat_decorator_sets_attribute_and_returns_function():
    # Positive count: decorator should attach the count and return the original function
    count = 3
    decorator = genty_repeat(count)

    def dummy(self):  # dummy test method
        pass

    wrapped = decorator(dummy)
    assert wrapped is dummy
    assert hasattr(wrapped, "genty_repeat_count")
    assert wrapped.genty_repeat_count == count

    # Zero count: still attaches attribute with value 0
    zero_decorator = genty_repeat(0)
    zero_wrapped = zero_decorator(dummy)
    assert zero_wrapped.genty_repeat_count == 0

    # Negative count: should raise ValueError
    with pytest.raises(ValueError):
        genty_repeat(-1)
