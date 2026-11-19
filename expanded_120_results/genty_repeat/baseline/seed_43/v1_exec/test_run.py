import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count_attribute():
    def dummy_test(self):
        """Dummy test method."""
        pass

    decorated = genty_repeat(4)(dummy_test)

    assert decorated is dummy_test
    assert hasattr(decorated, "genty_repeat_count")
    assert decorated.genty_repeat_count == 4
