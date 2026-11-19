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
    # a.value should exist; c.value should not exist
    assert hasattr(a, "value")
    with pytest.raises(AttributeError):
        _ = c.value


def test_map_on_nothing_and_value():
    m = Maybe.just(5)
    result = m.map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.get_or_else(-1) == 10

    n = Maybe.nothing()
    result_n = n.map(lambda x: x * 2)
    assert result_n.is_nothing
    assert result_n.get_or_else(99) == 99


def test_bind_with_success_and_failure():
    def to_maybe(x):
        return Maybe.just(x + 1) if x > 0 else Maybe.nothing()

    m = Maybe.just(3)
    res = m.bind(to_maybe)
    assert res.get_or_else(-1) == 4

    m_neg = Maybe.just(-1)
    res_neg = m_neg.bind(to_maybe)
    assert res_neg.is_nothing

    n = Maybe.nothing()
    res_n = n.bind(to_maybe)
    assert res_n.is_nothing


def test_ap_with_function_and_value():
    f = Maybe.just(lambda x: x * 3)
    v = Maybe.just(4)
    res = f.ap(v)
    assert res.get_or_else(0) == 12

    f_none = Maybe.nothing()
    res_none = f_none.ap(v)
    assert res_none.is_nothing

    v_none = Maybe.nothing()
    res_v_none = f.ap(v_none)
    assert res_v_none.is_nothing


def test_filter_accepts_and_rejects():
    m = Maybe.just(7)
    res_true = m.filter(lambda x: x > 5)
    assert res_true.get_or_else(-1) == 7

    res_false = m.filter(lambda x: x < 5)
    assert res_false.is_nothing

    n = Maybe.nothing()
    res_n = n.filter(lambda x: True)
    assert res_n.is_nothing


def test_get_or_else_returns_value_or_default():
    m = Maybe.just("hello")
    assert m.get_or_else("default") == "hello"

    n = Maybe.nothing()
    assert n.get_or_else("default") == "default"


def test_to_either_transforms_correctly():
    m = Maybe.just(42)
    e = m.to_either()
    assert isinstance(e, Right)
    assert e.value == 42

    n = Maybe.nothing()
    e_none = n.to_either()
    assert isinstance(e_none, Left)
    assert e_none.value is None


def test_to_box_transforms_correctly():
    m = Maybe.just("data")
    b = m.to_box()
    assert isinstance(b, Box)
    assert b.value == "data"

    n = Maybe.nothing()
    b_none = n.to_box()
    assert isinstance(b_none, Box)
    assert b_none.value is None


def test_to_lazy_returns_callable_and_evaluates():
    m = Maybe.just(99)
    l = m.to_lazy()
    assert isinstance(l, Lazy)
    # Lazy is callable; evaluate via __call__
    assert l() == 99

    n = Maybe.nothing()
    l_none = n.to_lazy()
    assert isinstance(l_none, Lazy)
    assert l_none() is None


def test_to_try_success_and_failure():
    m = Maybe.just("ok")
    t = m.to_try()
    assert isinstance(t, Try)
    assert t.is_success
    assert t.value == "ok"

    n = Maybe.nothing()
    t_none = n.to_try()
    assert isinstance(t_none, Try)
    assert not t_none.is_success
    assert t_none.value is None


def test_to_validation_success_and_none():
    m = Maybe.just(3.14)
    v = m.to_validation()
    assert isinstance(v, Validation)
    assert v.is_success
    assert v.value == 3.14

    n = Maybe.nothing()
    v_none = n.to_validation()
    assert isinstance(v_none, Validation)
    assert v_none.is_success
    assert v_none.value is None
