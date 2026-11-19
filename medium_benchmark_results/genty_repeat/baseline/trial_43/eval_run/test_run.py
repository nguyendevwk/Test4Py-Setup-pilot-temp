import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_attribute():
    @genty_repeat(3)
    def dummy():
        pass

    assert getattr(dummy, "genty_repeat_count") == 3
