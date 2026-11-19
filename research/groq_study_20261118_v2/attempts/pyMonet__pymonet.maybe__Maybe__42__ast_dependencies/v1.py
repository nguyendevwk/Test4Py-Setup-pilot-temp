import pytest
from pymonet.maybe import Maybe


def test_just_and_nothing_equality():
    a = Maybe.just(10)
    b = Maybe.just(10)
    c = Maybe.just(20)
    d = Maybe.nothing()
    e = Maybe.nothing()

    assert a == b
    assert a != c
    assert d == e
    assert a != d
    assert d != a


def test_map_on_nonempty_and_empty():
    m = Maybe.just(5)
    result = m.map(lambda x: x * 2)
    assert isinstance(result, Maybe)
    assert result.get_or_else(None) == 10

    n = Maybe.nothing()
    result_n = n.map(lambda x: x * 2)
    assert result_n.is_nothing
    assert result_n.get_or_else(99) == 99


def test_bind_on_nonempty_and_empty():
    m = Maybe.just(3)
    result = m.bind(lambda x: Maybe.just(x + 4))
    assert result.get_or_else(None) == 7

    n = Maybe.nothing()
    result_n = n.bind(lambda x: Maybe.just(x + 4))
    assert result_n.is_nothing
    assert result_n.get_or_else(0) == 0


def test_ap_with_function_and_value():
    f = Maybe.just(lambda x: x * 3)
    v = Maybe.just(7)
    result = f.ap(v)
    assert result.get_or_else(None) == 21

    nf = Maybe.nothing()
    result_nf = nf.ap(v)
    assert result_nf.is_nothing

    nv = Maybe.nothing()
    result_nv = f.ap(nv)
    assert result_nv.is_nothing


def test_filter_accepts_and_rejects():
    m = Maybe.just(4)
    passed = m.filter(lambda x: x > 0)
    assert passed.get_or_else(None) == 4

    failed = m.filter(lambda x: x > 10)
    assert failed.is_nothing
    assert failed.get_or_else(5) == 5

    n = Maybe.nothing()
    nf = n.filter(lambda x: True)
    assert nf.is_nothing


def test_get_or_else_returns_value_or_default():
    m = Maybe.just("hello")
    assert m.get_or_else("default") == "hello"

    n = Maybe.nothing()
    assert n.get_or_else("default") == "default"


def test_to_either_and_to_box_and_to_lazy_and_to_try_and_to_validation():
    m = Maybe.just(42)
    e = m.to_either()
    assert hasattr(e, "is_left") or hasattr(e, "is_right")
    assert e.value == 42

    b = m.to_box()
    assert hasattr(b, "value")
    assert b.value == 42

    l = m.to_lazy()
    assert hasattr(l, "value")
    assert l.value() == 42

    t = m.to_try()
    assert hasattr(t, "is_success")
    assert t.is_success
    assert t.value == 42

    v = m.to_validation()
    assert hasattr(v, "is_success")
    assert v.is_success
    assert v.value == 42

    n = Maybe.nothing()
    e_n = n.to_either()
    assert e_n.is_left
    assert e_n.value is None

    b_n = n.to_box()
    assert b_n.value is None

    l_n = n.to_lazy()
    assert l_n.value() is None

    t_n = n.to_try()
    assert not t_n.is_success
    assert t_n.value is None

    v_n = n.to_validation()
    assert v_n.is_success
    assert v_n.value is None
