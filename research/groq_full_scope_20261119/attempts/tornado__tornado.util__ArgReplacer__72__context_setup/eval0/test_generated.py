import pytest
from tornado.util import ArgReplacer

def test_replace_positional_argument():
    # Function with positional argument 'x'
    def func(x, y):
        return x + y

    replacer = ArgReplacer(func, "x")
    old, new_args, new_kwargs = replacer.replace(10, (1, 2), {})
    assert old == 1  # original value of x
    assert new_args == (10, 2)  # x replaced, y unchanged
    assert new_kwargs == {}  # no keyword arguments used

def test_replace_keyword_argument():
    # Function with keyword argument 'y'
    def func(x, y=5):
        return x * y

    replacer = ArgReplacer(func, "y")
    old, new_args, new_kwargs = replacer.replace(20, (3,), {})
    assert old == 5  # default value of y
    assert new_args == (3,)  # positional args unchanged
    assert new_kwargs == {"y": 20}  # y replaced via keyword

def test_replace_missing_argument():
    # Function with no 'z' argument
    def func(a, b):
        return a - b

    replacer = ArgReplacer(func, "z")
    old, new_args, new_kwargs = replacer.replace("new", (1, 2), {})
    assert old is None  # argument not present
    assert new_args == (1, 2)  # positional args unchanged
    assert new_kwargs == {"z": "new"}  # new keyword added
