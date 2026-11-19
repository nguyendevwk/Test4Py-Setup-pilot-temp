import pytest
from genty.genty_args import GentyArgs

def test_genty_args_iteration_and_properties():
    # Instantiate with mixed positional and keyword arguments
    ga = GentyArgs(1, "two", key="val", num=3, alpha="beta")

    # Verify stored args and kwargs
    assert ga.args == (1, "two")
    assert ga.kwargs == {"key": "val", "num": 3, "alpha": "beta"}

    # Iteration should yield formatted args first, then sorted kwargs
    iterated = list(ga)
    # Positional args formatted: 1 -> '1', "two" -> "'two'"
    assert iterated[0] == "1"
    assert iterated[1] == "'two'"

    # Keyword args sorted by key: alpha, key, num
    expected_kw = [
        "alpha='beta'",   # key 'alpha' with string value
        "key='val'",      # key 'key' with string value
        "num=3",          # key 'num' with int value
    ]
    assert iterated[2:] == expected_kw

    # All yielded items should be of type str
    assert all(isinstance(item, str) for item in iterated)
