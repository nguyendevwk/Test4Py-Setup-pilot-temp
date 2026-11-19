import sys
import types
import pytest
from collections import OrderedDict

# Provide a minimal stub for the missing `six` module
six_stub = types.ModuleType("six")
six_stub.PY2 = False
six_stub.PY3 = True
six_stub.string_types = (str,)
six_stub.text_type = str
six_stub.binary_type = bytes
six_stub.integer_types = (int,)
six_stub.iteritems = lambda d: d.items()
six_stub.itervalues = lambda d: d.values()
six_stub.iterkeys = lambda d: d.keys()
six_stub.moves = types.SimpleNamespace()
six_stub.moves.urllib = types.SimpleNamespace()
six_stub.moves.urllib.parse = types.SimpleNamespace()
six_stub.moves.urllib.parse.urlparse = lambda x: x
six_stub.moves.urllib.parse.urlunparse = lambda x: x
six_stub.moves.urllib.parse.urlencode = lambda x: x
six_stub.moves.urllib.parse.urljoin = lambda x, y: x + y
six_stub.moves.urllib.parse.quote = lambda x: x
six_stub.moves.urllib.parse.unquote = lambda x: x
six_stub.moves.urllib.parse.quote_plus = lambda x: x
six_stub.moves.urllib.parse.unquote_plus = lambda x: x
six_stub.moves.urllib.parse.parse_qs = lambda x: {}
six_stub.moves.urllib.parse.parse_qsl = lambda x: []
six_stub.moves.urllib.parse.urlsplit = lambda x: x
six_stub.moves.urllib.parse.urlunsplit = lambda x: x
sys.modules["six"] = six_stub

# Now import the target decorator
from genty.genty_dataset import genty_dataset

def test_genty_dataset_unnamed_datasets_conversion_and_storage():
    @genty_dataset(('x', 1), 'y', (2, 3))
    def dummy(a, b=None):
        pass

    # The decorator should return the original function unchanged
    assert dummy is not None

    # The function should now have a `genty_datasets` attribute
    assert hasattr(dummy, "genty_datasets")
    datasets = dummy.genty_datasets
    assert isinstance(datasets, OrderedDict)

    # Three datasets should have been added
    assert len(datasets) == 3

    # Each dataset must be stored as a tuple
    for key, dataset in datasets.items():
        assert isinstance(dataset, tuple)

        # The string representation of each element should appear in the key
        for elem in dataset:
            assert str(elem) in key

    # The single value 'y' should be stored as a one‑tuple
    assert datasets["y"] == ("y",)
