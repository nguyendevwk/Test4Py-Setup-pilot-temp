import pytest
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_behavior():
    # Unnamed arguments: each value becomes a separate dataset
    @genty_dataset('c1', 'c2')
    def func_unnamed(a):
        pass

    assert hasattr(func_unnamed, 'genty_datasets')
    assert len(func_unnamed.genty_datasets) == 2
    keys = list(func_unnamed.genty_datasets.keys())
    assert any('c1' in k for k in keys)
    assert any('c2' in k for k in keys)
    values = list(func_unnamed.genty_datasets.values())
    assert ('c1',) in values
    assert ('c2',) in values

    # Named arguments: key is the provided name
    @genty_dataset(happy=('a1', 'b1'))
    def func_named(a, b):
        pass

    assert func_named.genty_datasets['happy'] == ('a1', 'b1')

    # Overriding with the same named key: outer decorator wins
    def dummy(a):
        pass

    inner = genty_dataset(happy=('a1', 'b1'))(dummy)
    outer = genty_dataset(happy=('x1', 'y1'))(inner)
    assert outer.genty_datasets['happy'] == ('x1', 'y1')

    # Chaining unnamed decorators: both datasets are preserved
    def dummy2(a, b=None):
        pass

    chained = genty_dataset('x')(genty_dataset('y')(dummy2))
    assert len(chained.genty_datasets) == 2
    assert any('x' in k for k in chained.genty_datasets)
    assert any('y' in k for k in chained.genty_datasets)
