import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_behavior():
    # Unnamed single value dataset
    @genty_dataset('single')
    def func_single(): pass
    assert isinstance(func_single.genty_datasets, OrderedDict)
    assert list(func_single.genty_datasets.keys()) == ["'single'"]
    assert func_single.genty_datasets["'single'"] == ('single',)

    # Named dataset
    @genty_dataset(happy_path=('a1', 'b1'))
    def func_named(): pass
    assert list(func_named.genty_datasets.keys()) == ['happy_path']
    assert func_named.genty_datasets['happy_path'] == ('a1', 'b1')

    # Multiple unnamed datasets
    @genty_dataset(('a1', 'b1'), ('a2', 'b2'))
    def func_multiple(): pass
    assert list(func_multiple.genty_datasets.keys()) == ['a1, b1', 'a2, b2']
    assert func_multiple.genty_datasets['a1, b1'] == ('a1', 'b1')
    assert func_multiple.genty_datasets['a2, b2'] == ('a2', 'b2')

    # Chaining decorators with override (outer overrides inner)
    @genty_dataset('outer')
    @genty_dataset('inner')
    def func_chain(): pass
    assert list(func_chain.genty_datasets.keys()) == ['outer']
    assert func_chain.genty_datasets['outer'] == ('outer',)
    assert 'inner' not in func_chain.genty_datasets
