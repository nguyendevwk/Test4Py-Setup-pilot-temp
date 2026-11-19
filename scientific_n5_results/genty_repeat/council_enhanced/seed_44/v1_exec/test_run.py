import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_decorator_sets_attribute_and_returns_same_function():
    count = 7
    dec = genty_repeat(count)

    def original():
        pass

    decorated = dec(original)

    assert decorated is original
    assert decorated.genty_repeat_count == count
    assert decorated.__name__ == "original"
