import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_decorator_behavior():
    # Unnamed data sets
    @genty_dataset(('a1', 'b1'), ('a2', 'b2'))
    def func(a, b):
        pass

    expected = OrderedDict([('a1_and_b1', ('a1', 'b1')), ('a2_and_b2', ('a2', 'b2'))])
    assert func.genty_datasets == expected

    # Named data set
    @genty_dataset(happy_path=('c1', 'c2'))
    def func2(a, b):
        pass

    assert func2.genty_datasets == OrderedDict([('happy_path', ('c1', 'c2'))])

    # Chaining with outer overriding inner
    @genty_dataset(('x', 'y'))
    @genty_dataset(('p', 'q'), Monday=('a1', 'b1'))
    def func3(a, b):
        pass

    expected_chain = OrderedDict([
        ('p_and_q', ('p', 'q')),
        ('Monday', ('a1', 'b1')),
        ('x_and_y', ('x', 'y')),
    ])
    assert func3.genty_datasets == expected_chain

    # Conflict resolution: outer overrides inner
    @genty_dataset(conflict=('inner',))
    @genty_dataset(conflict=('outer',))
    def func4(a):
        pass

    assert func4.genty_datasets['conflict'] == ('outer',)
