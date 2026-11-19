import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_decorator_sets_repeat_count_and_returns_same_function():
    def original():
        pass

    decorated = genty_repeat(4)(original)
    assert decorated is original
    assert hasattr(decorated, "genty_repeat_count")
    assert decorated.genty_repeat_count == 4
