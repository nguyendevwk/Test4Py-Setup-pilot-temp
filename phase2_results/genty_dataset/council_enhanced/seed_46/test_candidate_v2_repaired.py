import sys
import types
from collections import OrderedDict

# Provide a minimal stub for the missing `six` module used by genty.
six_stub = types.SimpleNamespace(
    string_types=(str,),
    integer_types=(int,),
    text_type=str,
)
sys.modules["six"] = six_stub

from genty.genty_dataset import genty_dataset


def test_genty_dataset_stores_datasets_correctly():
    @genty_dataset(("x", 1), ("y", 2))
    def dummy(a, b):
        pass

    expected = OrderedDict([("x, 1", ("x", 1)), ("y, 2", ("y", 2))])
    assert dummy.genty_datasets == expected

    @genty_dataset("c")
    def dummy_single(a):
        pass

    assert dummy_single.genty_datasets == OrderedDict([("c", ("c",))])

    @genty_dataset(happy=("a", "b"))
    def dummy_named(a, b):
        pass

    assert dummy_named.genty_datasets == OrderedDict([("happy", ("a", "b"))])

    @genty_dataset(same=("outer",))
    @genty_dataset(same=("inner",))
    def dummy_chain():
        pass

    # The first decorator wins for duplicate keys.
    assert dummy_chain.genty_datasets["same"] == ("outer",)

    @genty_dataset(("x", 1), foo=("y", 2))
    def dummy_mix(a, b):
        pass

    assert dummy_mix.genty_datasets == OrderedDict([("x, 1", ("x", 1)), ("foo", ("y", 2))])
