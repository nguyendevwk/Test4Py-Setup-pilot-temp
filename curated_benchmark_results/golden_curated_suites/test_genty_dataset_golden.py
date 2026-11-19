import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset, format_arg


def test_genty_dataset_builds_and_overrides():
    # Test unnamed args and keyword args
    @genty_dataset(('a1', 'b1'), 5, key1=('x', 'y'), key2=10)
    def dummy(a, b=None):
        pass

    expected = OrderedDict()
    expected[format_arg('a1') + ", " + format_arg('b1')] = ('a1', 'b1')
    expected[format_arg(5)] = (5,)
    expected['key1'] = ('x', 'y')
    expected['key2'] = 10

    assert list(dummy.genty_datasets.keys()) == list(expected.keys())
    assert dummy.genty_datasets == expected

    # Test that outer decorator overrides inner when keys conflict
    @genty_dataset(dup=('outer',))
    @genty_dataset(dup=('inner',))
    def dummy_override():
        pass

    assert dummy_override.genty_datasets['dup'] == ('outer',)
