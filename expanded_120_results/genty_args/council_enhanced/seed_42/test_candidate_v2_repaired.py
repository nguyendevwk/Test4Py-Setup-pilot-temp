import sys
import types
import pytest

# Provide a minimal dummy `six` module to satisfy imports in the package.
sys.modules['six'] = types.SimpleNamespace()

from genty.genty_args import GentyArgs


def test_genty_args_iteration_and_properties():
    ga = GentyArgs(1, "two", key="val", num=3, alpha="beta")

    # Stored arguments
    assert ga.args == (1, "two")
    assert ga.kwargs == {"key": "val", "num": 3, "alpha": "beta"}

    # Iteration order and formatting
    iterated = list(ga)
    assert iterated[0] == "1"
    assert iterated[1] == "'two'"

    expected_kw = [
        "alpha='beta'",
        "key='val'",
        "num=3",
    ]
    assert iterated[2:] == expected_kw

    # All yielded items are strings
    assert all(isinstance(item, str) for item in iterated)
