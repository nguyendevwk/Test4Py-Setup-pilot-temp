import pytest
from itertools import chain
from genty.genty_args import GentyArgs, format_arg, format_kwarg


def test_genty_args_iteration_and_properties():
    # Arrange: create args and kwargs with unsorted keys
    args = (1, "two")
    kwargs = {"b": 2, "a": 1}

    # Act: instantiate GentyArgs
    g = GentyArgs(*args, **kwargs)

    # Assert: properties expose original data
    assert g.args == args
    assert g.kwargs == kwargs

    # Assert: iteration yields formatted args first, then sorted kwargs
    expected = list(
        chain(
            (format_arg(arg) for arg in args),
            (format_kwarg(k, v) for k, v in sorted(kwargs.items())),
        )
    )
    assert list(g) == expected
