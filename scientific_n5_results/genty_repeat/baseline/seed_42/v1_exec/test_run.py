import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(5)
    def dummy_test(self):
        pass

    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 5
