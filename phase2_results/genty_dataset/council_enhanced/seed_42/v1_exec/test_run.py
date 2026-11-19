import pytest
from genty.genty_dataset import genty_dataset


def test_genty_dataset_decorator_behavior():
    # Decorate a function with unnamed and named datasets
    @genty_dataset(('a1', 'b1'), 'c1', named=('x', 'y'))
    def dummy(a, b=None):
        pass

    # The decorator should attach an OrderedDict of datasets
    assert hasattr(dummy, 'genty_datasets')
    ds = dummy.genty_datasets
    # Order of insertion: unnamed first, then named
    assert list(ds.keys()) == ['a1, b1', 'c1', 'named']
    assert ds['a1, b1'] == ('a1', 'b1')
    assert ds['c1'] == ('c1',)          # single value turned into 1‑tuple
    assert ds['named'] == ('x', 'y')

    # Test that outer decorator overrides inner when keys collide
    @genty_dataset('dup')
    @genty_dataset('dup', dup=('inner',))
    def dummy2():
        pass

    ds2 = dummy2.genty_datasets
    # Only one key should remain, with the outer value
    assert list(ds2.keys()) == ['dup']
    assert ds2['dup'] == ('dup',)
