import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count_and_raises_on_negative():
    count = 3
    dec = genty_repeat(count)
    def dummy(self): pass
    wrapped = dec(dummy)
    assert wrapped is dummy
    assert wrapped.genty_repeat_count == count
    with pytest.raises(ValueError):
        genty_repeat(-1)
