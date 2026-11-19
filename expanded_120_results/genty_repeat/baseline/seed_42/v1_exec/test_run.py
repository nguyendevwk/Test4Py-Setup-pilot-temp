import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(5)
    def dummy_test(self):
        pass

    # The decorator should attach the repeat count to the function
    assert getattr(dummy_test, "genty_repeat_count", None) == 5
    # The returned object should be the original function
    assert dummy_test is dummy_test
