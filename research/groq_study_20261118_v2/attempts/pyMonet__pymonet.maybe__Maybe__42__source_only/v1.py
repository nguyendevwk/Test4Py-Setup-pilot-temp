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
    c = Maybe.nothing()
    d = Maybe.nothing()
    assert a == b
    assert c == d
    assert a != c
    assert a.is_nothing is False
    assert c.is_nothing is True
    # value attribute exists only for non‑nothing
    assert hasattr(a, "value") and a.value == 10
    assert not hasattr(c, "value")


def test_map_on_nonempty_and_empty():
    # mapping a value
    m = Maybe.just(5)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert mapped.is_nothing is False
    assert mapped.value == 10

    # mapping on nothing returns nothing
    n = Maybe.nothing()
    mapped_n = n.map(lambda x: x * 2)
    assert isinstance(mapped_n, Maybe)
    assert mapped_n.is_nothing is True
    assert not hasattr(mapped_n, "value")


def test_bind_with_success_and_failure():
    # bind that returns a new Maybe
    m = Maybe.just(3)
    bound = m.bind(lambda x: Maybe.just(x + 4))
    assert bound.is_nothing is False and bound.value == 7

    # bind that returns nothing
    bound_none = m.bind(lambda x: Maybe.nothing())
    assert bound_none.is_nothing is True

    # bind on nothing returns nothing
    n = Maybe.nothing()
    bound_n = n.bind(lambda x: Maybe.just(x))
    assert bound_n.is_nothing is True


def test_ap_with_function_and_value():
    # apply function inside Maybe to another Maybe
    f_maybe = Maybe.just(lambda x: x * 3)
    v_maybe = Maybe.just(4)
    result = f_maybe.ap(v_maybe)
    assert result.is_nothing is False and result.value == 12

    # apply on nothing returns nothing
    nothing_f = Maybe.nothing()
    result_nothing_f = nothing_f.ap(v_maybe)
    assert result_nothing_f.is_nothing is True

    # apply with nothing value
    nothing_v = Maybe.nothing()
    result_nothing_v = f_maybe.ap(nothing_v)
    assert result_nothing_v.is_nothing is True


def test_filter_accepts_and_rejects():
    m = Maybe.just(8)
    # filter that passes
    filtered = m.filter(lambda x: x > 5)
    assert filtered.is_nothing is False and filtered.value == 8

    # filter that fails
    filtered_fail = m.filter(lambda x: x < 5)
    assert filtered_fail.is_nothing is True

    # filter on nothing stays nothing
    n = Maybe.nothing()
    filtered_n = n.filter(lambda x: True)
    assert filtered_n.is_nothing is True


def test_get_or_else_returns_value_or_default():
    m = Maybe.just("hello")
    assert m.get_or_else("world") == "hello"

    n = Maybe.nothing()
    assert n.get_or_else("world") == "world"


def test_to_either_transforms_correctly():
    m = Maybe.just(42)
    e = m.to_either()
    assert isinstance(e, Right) and e.value == 42

    n = Maybe.nothing()
    e_none = n.to_either()
    assert isinstance(e_none, Left) and e_none.value is None


def test_to_box_transforms_correctly():
    m = Maybe.just("data")
    b = m.to_box()
    assert isinstance(b, Box) and b.value == "data"

    n = Maybe.nothing()
    b_none = n.to_box()
    assert isinstance(b_none, Box) and b_none.value is None


def test_to_lazy_returns_callable():
    m = Maybe.just(99)
    l = m.to_lazy()
    assert isinstance(l, Lazy)
    # Lazy is not callable; use its value attribute or get method
    assert getattr(l, "value", None) == 99 or getattr(l, "get", lambda: None)() == 99

    n = Maybe.nothing()
    l_none = n.to_lazy()
    assert isinstance(l_none, Lazy)
    assert getattr(l_none, "value", None) is None or getattr(l_none, "get", lambda: None)() is None


def test_to_try_success_and_failure():
    m = Maybe.just("ok")
    t = m.to_try()
    assert isinstance(t, Try) and t.is_success is True and t.value == "ok"

    n = Maybe.nothing()
    t_none = n.to_try()
    assert isinstance(t_none, Try) and t_none.is_success is False and t_none.value is None


def test_to_validation_success_and_none():
    m = Maybe.just(7)
    v = m.to_validation()
    # Validation may expose success via method or attribute
    is_success = getattr(v, "is_success", lambda: False)()
    assert isinstance(v, Validation) and is_success is True and v.value == 7

    n = Maybe.nothing()
    v_none = n.to_validation()
    is_success_none = getattr(v_none, "is_success", lambda: False)()
    assert isinstance(v_none, Validation) and is_success_none is True and v_none.value is None
