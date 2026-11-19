import pytest
from genty.genty_args import GentyArgs, format_arg, format_kwarg

def test_genty_args_iteration_and_properties():
    args = (1, "two", 3.0)
    kwargs = {"key2": 2, "key1": "value1"}
    g = GentyArgs(*args, **kwargs)

    # Verify stored args and kwargs
    assert g.args == args
    assert g.kwargs == kwargs

    # Expected iteration order: args first, then sorted kwargs formatted
    expected = [format_arg(a) for a in args] + [
        format_kwarg(k, v) for k, v in sorted(kwargs.items())
    ]

    actual = list(g)
    assert actual == expected
    assert all(isinstance(item, str) for item in actual)
