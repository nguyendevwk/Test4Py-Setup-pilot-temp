import sys
import types
import pytest

# Provide a minimal six stub to satisfy genty imports
six_stub = types.ModuleType("six")
six_stub.string_types = (str,)
six_stub.text_type = str
six_stub.integer_types = (int,)
six_stub.binary_type = bytes
six_stub.PY2 = False
six_stub.PY3 = True
six_stub.iteritems = lambda d: d.items()
six_stub.itervalues = lambda d: d.values()
six_stub.iterkeys = lambda d: d.keys()
def reraise(exc, val, tb):
    raise val.with_traceback(tb)
six_stub.reraise = reraise
sys.modules["six"] = six_stub

from genty.genty_repeat import genty_repeat

def test_genty_repeat_decorator_sets_attribute_and_returns_same_function():
    count = 7
    dec = genty_repeat(count)

    def original():
        pass

    decorated = dec(original)

    assert decorated is original
    assert getattr(decorated, "genty_repeat_count") == count
    assert decorated.__name__ == "original"
