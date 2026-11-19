import pytest
from tornado.util import ArgReplacer

def test_replace_positional_argument():
    # Function with positional argument 'x'
    def func(x, y):
        return x + y

    replacer = ArgReplacer(func, "x")
    # Original args: x=10, y=5
    old, new_args, new_kwargs = replacer.replace(20, (10, 5), {})
    assert old == 10
    assert new_args == (20, 5)
    assert new_kwargs == {}

def test_replace_keyword_argument():
    # Function with keyword argument 'z'
    def func(a, b, z=0):
        return a * b + z

    replacer = ArgReplacer(func, "z")
    # Original kwargs: z=3
    old, new_args, new_kwargs = replacer.replace(10, (2, 3), {"z": 3})
    assert old == 3
    assert new_args == (2, 3)
    assert new_kwargs == {"z": 10}

def test_replace_missing_argument_adds_to_kwargs():
    # Function with no 'missing' parameter
    def func(a, b):
        return a - b

    replacer = ArgReplacer(func, "missing")
    # No 'missing' in args or kwargs
    old, new_args, new_kwargs = replacer.replace(99, (1, 2), {})
    assert old is None
    assert new_args == (1, 2)
    assert new_kwargs == {"missing": 99}
