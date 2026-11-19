import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count_attribute():
    # Arrange: define a dummy test function
    def dummy_test(self):
        pass

    # Act: apply the decorator with a positive count
    decorated = genty_repeat(5)(dummy_test)

    # Assert: the decorator returns the original function
    assert decorated is dummy_test

    # Assert: the function now has the expected attribute set by the decorator
    assert hasattr(decorated, "genty_repeat_count")
    assert decorated.genty_repeat_count == 5
