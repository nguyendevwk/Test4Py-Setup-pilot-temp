import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_behavior():
    # Negative count should raise ValueError
    with pytest.raises(ValueError):
        genty_repeat(-5)

    # Positive count should set the attribute on the wrapped test method
    count = 4
    @genty_repeat(count)
    def dummy_test(self):
        pass

    assert getattr(dummy_test, "genty_repeat_count") == count
