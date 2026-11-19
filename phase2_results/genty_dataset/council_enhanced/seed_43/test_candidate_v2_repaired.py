import sys
import types
import pytest

# Provide a minimal six stub so genty can import it
six_stub = types.ModuleType("six")
six_stub.string_types = (str,)
six_stub.text_type = str
six_stub.binary_type = bytes
six_stub.integer_types = (int,)
six_stub.PY2 = False
six_stub.PY3 = True
six_stub.iteritems = lambda d: d.items()
six_stub.iterkeys = lambda d: d.keys()
six_stub.itervalues = lambda d: d.values()
six_stub.reraise = lambda exc, val, tb: exc(val).with_traceback(tb)
six_stub.add_metaclass = lambda cls: cls
six_stub.with_metaclass = lambda *args, **kwargs: lambda cls: cls
six_stub.wraps = lambda f: f
six_stub.raise_from = lambda exc, cause: exc
sys.modules["six"] = six_stub

from genty.genty_dataset import genty_dataset

def test_genty_dataset_duplicate_key_overridden_by_outer():
    @genty_dataset(dup="outer")
    @genty_dataset(dup="inner")
    def func():
        pass

    assert hasattr(func, "genty_datasets")
    assert "dup" in func.genty_datasets
    assert func.genty_datasets["dup"] == ("outer",)
