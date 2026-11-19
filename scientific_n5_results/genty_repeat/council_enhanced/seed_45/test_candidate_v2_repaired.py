import sys
import types
import pytest

# Provide a minimal stub for the missing `six` dependency
six_stub = types.SimpleNamespace(
    string_types=(str,),
    integer_types=(int,),
    text_type=str,
    binary_type=bytes,
    iteritems=lambda d: d.items(),
    itervalues=lambda d: d.values(),
    iterkeys=lambda d: d.keys(),
)
sys.modules["six"] = six_stub

from genty.genty_repeat import genty_repeat

def test_genty_repeat_sets_repeat_count_attribute():
    count = 4

    @genty_repeat(count)
    def test_func():
        return "ok"

    assert getattr(test_func, "genty_repeat_count", None) == count
    assert test_func() == "ok"
