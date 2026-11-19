import sys
import types
import pytest

# Provide a minimal stub for the missing `six` module so that genty imports successfully.
six_stub = types.SimpleNamespace(
    iteritems=lambda d: d.items(),
    string_types=(str,),
    text_type=str,
    binary_type=bytes,
    PY3=True,
)
sys.modules["six"] = six_stub

# Now import the target class.
from genty.genty_args import GentyArgs


def test_genty_args_properties_and_iteration():
    g = GentyArgs(1, "two", 3.0, flag=True, name="Alice")

    # Positional and keyword arguments are stored correctly.
    assert isinstance(g.args, tuple)
    assert g.args == (1, "two", 3.0)
    assert isinstance(g.kwargs, dict)
    assert g.kwargs == {"flag": True, "name": "Alice"}

    # Iteration yields formatted positional args followed by sorted keyword args.
    iterated = list(g)
    assert iterated == ["1", "'two'", "3.0", "flag=True", "name='Alice'"]
    assert iterated[:3] == ["1", "'two'", "3.0"]
    assert iterated[3:] == ["flag=True", "name='Alice'"]

    # Empty GentyArgs behaves correctly.
    empty = GentyArgs()
    assert empty.args == ()
    assert empty.kwargs == {}
    assert list(empty) == []
