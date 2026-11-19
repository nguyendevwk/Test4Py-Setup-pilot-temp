import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count():
    @genty_repeat(5)
    def dummy_test(self):
        """Dummy test function to verify genty_repeat decorator."""
        pass

    # The decorator should attach the repeat count to the function
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 5

    # The decorator should return the original function object unchanged
    assert callable(dummy_test)
