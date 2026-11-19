import pytest
from genty.genty_args import GentyArgs, format_arg, format_kwarg


def test_genty_args_iteration_and_properties():
    # Arrange: create GentyArgs with mixed positional and keyword arguments
    pos_args = (1, "two", 3.0)
    kw_args = {"b": 2, "a": 1, "c": 3}
    genty = GentyArgs(*pos_args, **kw_args)

    # Assert that the args property returns the original tuple
    assert genty.args == pos_args
    # Assert that the kwargs property returns the original dict
    assert genty.kwargs == kw_args

    # Compute expected formatted strings using the same helper functions
    expected = [format_arg(arg) for arg in pos_args]
    expected += [format_kwarg(k, v) for k, v in sorted(kw_args.items())]

    # Iterate over GentyArgs and compare to expected list
    assert list(genty) == expected

    # Verify that the keyword part is sorted by key
    kw_part = [item for item in list(genty) if "=" in item]
    assert kw_part[0] == format_kwarg("a", 1)
    assert kw_part[1] == format_kwarg("b", 2)
    assert kw_part[2] == format_kwarg("c", 3)

    # Verify that an empty GentyArgs yields an empty iterator
    empty = GentyArgs()
    assert list(empty) == []
