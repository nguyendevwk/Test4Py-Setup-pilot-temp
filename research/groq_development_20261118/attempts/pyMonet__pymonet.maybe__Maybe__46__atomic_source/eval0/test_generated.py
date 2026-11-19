import pytest
from pymonet.maybe import Maybe
from pymonet.either import Left, Right
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation


def test_map_and_bind_behavior():
    # Create a non‑empty Maybe and apply map and bind
    m = Maybe.just(10)
    # map should apply function and wrap result
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert mapped.is_nothing is False
    assert mapped.value == 20

    # bind should apply function that returns a Maybe
    bound = m.bind(lambda x: Maybe.just(x + 5))
    assert bound == Maybe.just(15)

    # bind with a function returning Nothing
    bound_nothing = m.bind(lambda _: Maybe.nothing())
    assert bound_nothing.is_nothing is True
    assert bound_nothing == Maybe.nothing()


def test_filter_and_get_or_else():
    # Nothing case
    nothing = Maybe.nothing()
    assert nothing.filter(lambda x: x > 0) == Maybe.nothing()
    assert nothing.get_or_else(42) == 42

    # Some case with filter passing
    some = Maybe.just(3)
    filtered = some.filter(lambda x: x > 0)
    assert filtered == Maybe.just(3)

    # Some case with filter failing
    filtered_none = some.filter(lambda x: x < 0)
    assert filtered_none.is_nothing is True
    assert filtered_none == Maybe.nothing()

    # get_or_else on Some
    assert some.get_or_else(99) == 3


def test_conversion_to_other_monads(tmp_path):
    # Convert a non‑empty Maybe to various monads
    m = Maybe.just("hello")
    either = m.to_either()
    assert isinstance(either, Right)
    assert either.value == "hello"

    box = m.to_box()
    assert isinstance(box, Box)
    assert box.value == "hello"

    lazy = m.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.run() == "hello"

    try_monad = m.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success is True
    assert try_monad.value == "hello"

    validation = m.to_validation()
    assert isinstance(validation, Validation)
    assert validation.is_success is True
    assert validation.value == "hello"

    # Convert a Nothing Maybe
    n = Maybe.nothing()
    assert n.to_either() == Left(None)
    assert n.to_box() == Box(None)
    assert n.to_lazy().run() is None
    assert n.to_try().is_success is False
    assert n.to_validation().is_success is True
    assert n.to_validation().value is None
