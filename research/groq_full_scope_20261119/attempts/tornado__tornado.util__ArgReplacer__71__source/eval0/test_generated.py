import pytest
from tornado.util import ArgReplacer


def test_replace_positional_argument():
    def sample(a, b, c=3):
        return a, b, c

    replacer = ArgReplacer(sample, "b")
    old, new_args, new_kwargs = replacer.replace(99, (1, 2), {})
    assert old == 2
    assert new_args == (1, 99)
    assert new_kwargs == {}
    assert sample(*new_args, **new_kwargs) == (1, 99, 3)


def test_replace_keyword_argument():
    def sample(a, b, c=3):
        return a, b, c

    replacer = ArgReplacer(sample, "c")
    old, new_args, new_kwargs = replacer.replace(42, (1,), {"b": 2})
    assert old == 3
    assert new_args == (1,)
    assert new_kwargs == {"b": 2, "c": 42}
    assert sample(*new_args, **new_kwargs) == (1, 2, 42)


def test_replace_missing_argument_adds_to_kwargs():
    def sample(a, b):
        return a, b

    replacer = ArgReplacer(sample, "c")
    old, new_args, new_kwargs = replacer.replace("new", (1, 2), {})
    assert old is None
    assert new_args == (1, 2)
    assert new_kwargs == {"c": "new"}
    # The original function does not accept 'c', so we test that the
    # replacement does not alter the function's behavior when called
    # with the original arguments.
    assert sample(*new_args, **new_kwargs) == (1, 2)
