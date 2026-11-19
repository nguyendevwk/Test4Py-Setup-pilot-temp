import pytest
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_behavior():
    @genty_dataset(('first', 5), ('second', 6))
    def func1(a, b): pass
    assert hasattr(func1, 'genty_datasets')
    assert list(func1.genty_datasets.keys()) == ['first, 5', 'second, 6']
    assert func1.genty_datasets['first, 5'] == ('first', 5)

    @genty_dataset('only')
    def func2(a): pass
    assert list(func2.genty_datasets.keys()) == ['only']
    assert func2.genty_datasets['only'] == ('only',)

    @genty_dataset(happy=('a', 'b'))
    def func3(a, b): pass
    assert list(func3.genty_datasets.keys()) == ['happy']
    assert func3.genty_datasets['happy'] == ('a', 'b')

    @genty_dataset(dup='outer')
    @genty_dataset(dup='inner')
    def func4(): pass
    assert func4.genty_datasets['dup'] == ('outer',)

    @genty_dataset(1, 2)
    def func5(a): pass
    assert list(func5.genty_datasets.keys()) == ['1', '2']
    assert func5.genty_datasets['1'] == (1,)
