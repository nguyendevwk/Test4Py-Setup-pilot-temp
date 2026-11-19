import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(4)
    def dummy_test():
        pass

    # The decorator should attach the repeat count to the test method
    assert hasattr(dummy_test, "genty_repeat_count")
    assert dummy_test.genty_repeat_count == 4
