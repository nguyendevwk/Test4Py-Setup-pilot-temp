import pytest
from tornado.util import ArgReplacer

def test_replace_positional_argument():
    def func(a, b, c):
        return a, b, c

    replacer = ArgReplacer(func, "b")
    old, new_args, new_kwargs = replacer.replace(99, (1, 2, 3), {})
    assert old == 2
    assert new_args == (1, 99, 3)
    assert new_kwargs == {}

def test_replace_keyword_argument():
    def func(a, b, c):
        return a, b, c

    replacer = ArgReplacer(func, "c")
    old, new_args, new_kwargs = replacer.replace(42, (1,), {"b": 2, "c": 3})
    assert old == 3
    assert new_args == (1,)
    assert new_kwargs == {"b": 2, "c": 42}

def test_replace_missing_argument():
    def func(a, b):
        return a, b

    replacer = ArgReplacer(func, "c")
    old, new_args, new_kwargs = replacer.replace("new", (1, 2), {})
    assert old is None
    assert new_args == (1, 2)
    assert new_kwargs == {"c": "new"}
