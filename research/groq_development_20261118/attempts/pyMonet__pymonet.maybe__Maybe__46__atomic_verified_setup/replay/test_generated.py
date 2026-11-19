import pytest
from pymonet.maybe import Maybe

def test_map_on_nonempty_and_empty():
    # Non-empty Maybe: map should apply function
    m = Maybe.just(10)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert not mapped.is_nothing
    assert mapped.value == 20

    # Empty Maybe: map should return empty
    empty = Maybe.nothing()
    mapped_empty = empty.map(lambda x: x * 2)
    assert isinstance(mapped_empty, Maybe)
    assert mapped_empty.is_nothing

def test_bind_returns_maybe_and_propagates_empty():
    # bind with function returning Maybe
    m = Maybe.just(5)
    result = m.bind(lambda x: Maybe.just(x + 3))
    assert isinstance(result, Maybe)
    assert not result.is_nothing
    assert result.value == 8

    # bind on empty should propagate empty
    empty = Maybe.nothing()
    result_empty = empty.bind(lambda x: Maybe.just(x + 3))
    assert isinstance(result_empty, Maybe)
    assert result_empty.is_nothing

def test_get_or_else_returns_value_or_default():
    # Non-empty returns stored value
    m = Maybe.just("hello")
    assert m.get_or_else("default") == "hello"

    # Empty returns default
    empty = Maybe.nothing()
    assert empty.get_or_else("default") == "default"
