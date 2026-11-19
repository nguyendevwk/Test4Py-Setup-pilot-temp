import pytest
from pymonet.maybe import Maybe

def test_map_on_nonempty_and_empty():
    # Non-empty Maybe: map should apply function and wrap result
    m = Maybe.just(10)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert not mapped.is_nothing
    assert mapped.value == 20

    # Empty Maybe: map should return a new empty Maybe
    empty = Maybe.nothing()
    mapped_empty = empty.map(lambda x: x * 2)
    assert isinstance(mapped_empty, Maybe)
    assert mapped_empty.is_nothing
    assert mapped_empty == Maybe.nothing()

def test_bind_returns_maybe_and_propagates_nothing():
    # bind with a function that returns a Maybe
    m = Maybe.just(5)
    bound = m.bind(lambda x: Maybe.just(x + 3))
    assert isinstance(bound, Maybe)
    assert not bound.is_nothing
    assert bound.value == 8

    # bind on empty should propagate Nothing
    empty = Maybe.nothing()
    bound_empty = empty.bind(lambda x: Maybe.just(x + 3))
    assert bound_empty.is_nothing
    assert bound_empty == Maybe.nothing()

def test_get_or_else_and_equality():
    # get_or_else on non-empty returns stored value
    m = Maybe.just("hello")
    assert m.get_or_else("default") == "hello"

    # get_or_else on empty returns default
    empty = Maybe.nothing()
    assert empty.get_or_else("default") == "default"

    # Equality checks: same value and same emptiness
    m2 = Maybe.just("hello")
    assert m == m2
    assert m != Maybe.just("world")
    assert empty == Maybe.nothing()
    assert empty != m
