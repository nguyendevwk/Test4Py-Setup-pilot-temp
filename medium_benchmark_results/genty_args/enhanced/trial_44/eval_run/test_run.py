import pytest
from genty.genty_args import genty_args


def test_genty_args_iteration_and_properties():
    # Create GentyArgs with mixed positional and keyword arguments
    ga = genty_args(1, "two", b="bee", a=1)

    # The args property should return the original positional arguments as a tuple
    assert ga.args == (1, "two")
    assert isinstance(ga.args, tuple)

    # The kwargs property should return the original keyword arguments as a dict
    assert ga.kwargs == {"b": "bee", "a": 1}
    assert isinstance(ga.kwargs, dict)

    # Iteration should yield formatted positional arguments first,
    # followed by keyword arguments sorted by key and formatted as key=value
    expected_iteration = ["1", "'two'", "a=1", "b='bee'"]
    assert list(ga) == expected_iteration
