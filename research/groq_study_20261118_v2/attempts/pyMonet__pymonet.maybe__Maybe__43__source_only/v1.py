import pytest
from pymonet.maybe import Maybe
from pymonet.either import Left, Right
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation


def test_just_and_nothing_equality_and_identity():
    a = Maybe.just(10)
    b = Maybe.just(10)
    c = Maybe.just(20)
    d = Maybe.nothing()
    e = Maybe.nothing()

    assert a == b
    assert a != c
    assert d == e
    assert a != d
    assert a.is_nothing is False
    assert d.is_nothing is True


def test_map_on_nothing_returns_nothing():
    m = Maybe.nothing()
    result = m.map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.is_nothing
    assert result == Maybe.nothing()


def test_map_on_value_applies_function():
    m = Maybe.just(5)
    result = m.map(lambda x: x + 3)
    assert result.is_nothing is False
    assert result.get_or_else(None) == 8
    assert result == Maybe.just(8)


def test_bind_on_nothing_returns_nothing():
    m = Maybe.nothing()
    result = m.bind(lambda x: Maybe.just(x * 2))
    assert result.is_nothing
    assert result == Maybe.nothing()


def test_bind_on_value_returns_mapper_result():
    m = Maybe.just(4)
    result = m.bind(lambda x: Maybe.just(x * 3))
    assert result == Maybe.just(12)


def test_ap_with_nothing_returns_nothing():
    m = Maybe.nothing()
    applicative = Maybe.just(lambda x: x + 1)
    result = m.ap(applicative)
    assert result.is_nothing
    assert result == Maybe.nothing()


def test_ap_with_value_applies_function():
    m = Maybe.just(lambda x: x * 2)
    applicative = Maybe.just(7)
    result = m.ap(applicative)
    assert result == Maybe.just(14)


def test_filter_on_nothing_returns_nothing():
    m = Maybe.nothing()
    result = m.filter(lambda x: x > 0)
    assert result.is_nothing
    assert result == Maybe.nothing()


def test_filter_on_value_falsey_returns_nothing():
    m = Maybe.just(0)
    result = m.filter(lambda x: x > 0)
    assert result.is_nothing
    assert result == Maybe.nothing()


def test_filter_on_value_truthy_returns_same():
    m = Maybe.just(5)
    result = m.filter(lambda x: x > 0)
    assert result == m
    assert result.get_or_else(None) == 5


def test_get_or_else_on_nothing_and_value():
    n = Maybe.nothing()
    v = Maybe.just(42)
    assert n.get_or_else(99) == 99
    assert v.get_or_else(99) == 42


def test_to_either_conversion():
    n = Maybe.nothing()
    v = Maybe.just("ok")
    assert isinstance(n.to_either(), Left)
    assert n.to_either().value is None
    assert isinstance(v.to_either(), Right)
    assert v.to_either().value == "ok"


def test_to_box_conversion():
    n = Maybe.nothing()
    v = Maybe.just(3.14)
    assert isinstance(n.to_box(), Box)
    assert n.to_box().value is None
    assert isinstance(v.to_box(), Box)
    assert v.to_box().value == 3.14


def test_to_lazy_conversion():
    n = Maybe.nothing()
    v = Maybe.just("lazy")
    lazy_n = n.to_lazy()
    lazy_v = v.to_lazy()
    assert isinstance(lazy_n, Lazy)
    assert lazy_n.value is None
    assert isinstance(lazy_v, Lazy)
    assert lazy_v.value == "lazy"


def test_to_try_conversion():
    n = Maybe.nothing()
    v = Maybe.just("try")
    try_n = n.to_try()
    try_v = v.to_try()
    assert isinstance(try_n, Try)
    assert not try_n.is_success
    assert try_n.value is None
    assert isinstance(try_v, Try)
    assert try_v.is_success
    assert try_v.value == "try"


def test_to_validation_conversion():
    n = Maybe.nothing()
    v = Maybe.just("valid")
    val_n = n.to_validation()
    val_v = v.to_validation()
    assert isinstance(val_n, Validation)
    assert val_n.is_success
    assert val_n.value is None
    assert isinstance(val_v, Validation)
    assert val_v.is_success
    assert val_v.value == "valid"
