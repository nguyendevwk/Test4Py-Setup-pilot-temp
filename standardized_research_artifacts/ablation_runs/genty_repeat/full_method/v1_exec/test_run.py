import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_decorator_sets_attribute_and_returns_same_function():
    count = 3
    dec = genty_repeat(count)

    def dummy_test(self):
        pass

    # Apply the decorator
    decorated = dec(dummy_test)

    # The decorator should return the original function unchanged
    assert decorated is dummy_test

    # The function should now have the genty_repeat_count attribute set correctly
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == count
