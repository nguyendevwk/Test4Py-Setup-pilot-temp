import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_attaches_and_overrides():
    @genty_dataset('c1', 'c2')
    def dummy(a):
        pass

    assert hasattr(dummy, 'genty_datasets')
    assert isinstance(dummy.genty_datasets, OrderedDict)
    assert list(dummy.genty_datasets.keys()) == ['c1', 'c2']
    assert dummy.genty_datasets['c1'] == ('c1',)
    assert dummy.genty_datasets['c2'] == ('c2',)

    @genty_dataset(('a1', 'b1'), ('a2', 'b2'))
    def dummy2(a, b):
        pass

    assert list(dummy2.genty_datasets.keys()) == ['a1b1', 'a2b2']
    assert dummy2.genty_datasets['a1b1'] == ('a1', 'b1')

    @genty_dataset(dup=('outer',))
    @genty_dataset(dup=('inner',))
    def dummy3(x):
        pass

    assert dummy3.genty_datasets['dup'] == ('outer',)
