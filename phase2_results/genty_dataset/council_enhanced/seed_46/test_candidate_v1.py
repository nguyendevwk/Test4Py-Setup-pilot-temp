from collections import OrderedDict
from genty.genty_dataset import genty_dataset

def test_genty_dataset_behavior():
    @genty_dataset(('x', 1), ('y', 2))
    def dummy(a, b):  # noqa: D401
        pass

    expected = OrderedDict()
    for dataset in [('x', 1), ('y', 2)]:
        suffix = ', '.join(map(str, dataset))
        expected[suffix] = dataset
    assert dummy.genty_datasets == expected

    @genty_dataset('c')
    def dummy_single(a):  # noqa: D401
        pass
    assert dummy_single.genty_datasets == OrderedDict([('c', ('c',))])

    @genty_dataset(happy=('a', 'b'))
    def dummy_named(a, b):  # noqa: D401
        pass
    assert dummy_named.genty_datasets == OrderedDict([('happy', ('a', 'b'))])

    @genty_dataset(same=('outer',))
    @genty_dataset(same=('inner',))
    def dummy_chain():  # noqa: D401
        pass
    assert dummy_chain.genty_datasets['same'] == ('outer',)

    @genty_dataset(('x', 1), foo=('y', 2))
    def dummy_mix(a, b):  # noqa: D401
        pass
    assert dummy_mix.genty_datasets == OrderedDict([('x, 1', ('x', 1)), ('foo', ('y', 2))])
