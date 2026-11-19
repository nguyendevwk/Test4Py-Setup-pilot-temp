import pytest
from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_outer_overrides_inner():
    @genty_dataset(('x', 'y'), Monday=('a1', 'b1'))
    @genty_dataset(('p', 'q'), Monday=('c1', 'd1'))
    def dummy(a, b):
        pass

    expected = OrderedDict([
        ('p_and_q', ('p', 'q')),
        ('Monday', ('a1', 'b1')),
        ('x_and_y', ('x', 'y')),
    ])

    assert dummy.genty_datasets == expected
