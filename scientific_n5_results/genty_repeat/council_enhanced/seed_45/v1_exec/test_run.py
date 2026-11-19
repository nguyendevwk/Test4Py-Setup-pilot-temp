import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_repeat_count_attribute():
    count = 4
    @genty_repeat(count)
    def test_func():
        return "ok"

    assert test_func.genty_repeat_count == count
    assert test_func() == "ok"
