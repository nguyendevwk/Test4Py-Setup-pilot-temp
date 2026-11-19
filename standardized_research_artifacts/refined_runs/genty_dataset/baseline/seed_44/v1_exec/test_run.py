from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_outer_overrides_inner():
    @genty_dataset(a=('inner_a', 'inner_b'))
    @genty_dataset(a=('outer_a', 'outer_b'))
    def dummy(a, b):
        return a, b

    assert hasattr(dummy, 'genty_datasets')
    assert isinstance(dummy.genty_datasets, OrderedDict)
    assert dummy.genty_datasets['a'] == ('outer_a', 'outer_b')
    assert dummy('x', 'y') == ('x', 'y')
