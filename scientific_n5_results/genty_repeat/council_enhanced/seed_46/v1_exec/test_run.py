import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_count_and_raises():
    # Positive count: decorator should attach the count and return the original function
    count = 3
    dec = genty_repeat(count)
    def dummy(self): pass
    wrapped = dec(dummy)
    assert wrapped is dummy
    assert getattr(dummy, "genty_repeat_count") == count

    # Zero count: still valid, attribute set to 0
    zero_dec = genty_repeat(0)
    def zero_dummy(self): pass
    zero_wrapped = zero_dec(zero_dummy)
    assert zero_wrapped is zero_dummy
    assert zero_dummy.genty_repeat_count == 0

    # Negative count: should raise ValueError
    with pytest.raises(ValueError):
        genty_repeat(-1)
