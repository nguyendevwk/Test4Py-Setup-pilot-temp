import pytest
from genty.genty_args import GentyArgs

def test_genty_args_iteration_and_properties():
    args = (1, "foo")
    kwargs = {"b": 2, "a": "bar"}
    g = GentyArgs(*args, **kwargs)

    # Check that the stored args and kwargs are returned correctly
    assert g.args == args
    assert g.kwargs == kwargs

    # Iterate over the GentyArgs instance and collect the formatted strings
    iterated = list(g)
    expected = ["1", "'foo'", "a='bar'", "b=2"]

    # Verify the iteration order: args first, then sorted kwargs
    assert iterated == expected
    assert iterated[0] == "1"
    assert iterated[1] == "'foo'"
    assert iterated[2] == "a='bar'"
    assert iterated[3] == "b=2"
