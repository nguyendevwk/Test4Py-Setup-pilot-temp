import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(3)
    def dummy_test(self):
        pass

    # The decorator should attach the repeat count to the function
    assert getattr(dummy_test, "genty_repeat_count", None) == 3
    # The function object should remain unchanged
    assert dummy_test.__name__ == "dummy_test"
