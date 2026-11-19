import pytest
from pymonet.maybe import Maybe
from pymonet.either import Left, Right
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation

def test_map_and_get_or_else():
    # Create a non-empty Maybe and map over it
    m = Maybe.just(10)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert not mapped.is_nothing
    assert mapped.value == 20

    # get_or_else should return the value for non-empty Maybe
    assert mapped.get_or_else(0) == 20

    # Map over an empty Maybe returns an empty Maybe
    empty = Maybe.nothing()
    mapped_empty = empty.map(lambda x: x * 2)
    assert isinstance(mapped_empty, Maybe)
    assert mapped_empty.is_nothing
    assert mapped_empty.get_or_else(5) == 5

def test_bind_and_filter():
    # bind should apply a function returning a Maybe
    m = Maybe.just(3)
    bound = m.bind(lambda x: Maybe.just(x + 4))
    assert bound == Maybe.just(7)

    # bind on empty returns empty
    empty = Maybe.nothing()
    assert empty.bind(lambda x: Maybe.just(x + 4)) == Maybe.nothing()

    # filter keeps value when predicate true
    filtered = m.filter(lambda x: x > 2)
    assert filtered == Maybe.just(3)

    # filter returns empty when predicate false
    filtered_none = m.filter(lambda x: x < 0)
    assert filtered_none.is_nothing

def test_conversions_to_other_monads():
    # Non-empty Maybe conversions
    m = Maybe.just("hello")
    assert m.to_either() == Right("hello")
    assert m.to_box() == Box("hello")
    assert m.to_lazy().value() == "hello"
    assert m.to_try().is_success
    assert m.to_validation().is_success
    assert m.to_validation().value == "hello"

    # Empty Maybe conversions
    empty = Maybe.nothing()
    assert empty.to_either() == Left(None)
    assert empty.to_box() == Box(None)
    assert empty.to_lazy().value() is None
    assert not empty.to_try().is_success
    assert empty.to_validation().is_success
    assert empty.to_validation().value is None
