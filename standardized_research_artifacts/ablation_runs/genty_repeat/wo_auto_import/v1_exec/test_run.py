import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    count = 5
    dec = genty_repeat(count)

    def dummy(self):
        pass

    decorated = dec(dummy)

    assert decorated is dummy
    assert hasattr(decorated, "genty_repeat_count")
    assert decorated.genty_repeat_count == count
