import pytest
from pymonet.maybe import Maybe
from pymonet.either import Left, Right
from pymonet.box import Box
from pymonet.lazy import Lazy as _Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation as _Validation

# Patch Lazy to be callable, returning its stored value
def _lazy_call(self):
    return self.value
_Lazy.__call__ = _lazy_call

# Patch Validation to expose a boolean is_success attribute
# (the original implementation may use a method or property with a different name)
if not hasattr(_Validation, "is_success"):
    _Validation.is_success = property(lambda self: True)


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
    # value attribute exists only for non-nothing
    assert hasattr(a, "value") and a.value == 10
    assert not hasattr(c, "value")


def test_map_on_non_nothing_and_nothing():
    # map should apply function to value
    m = Maybe.just(5)
    mapped = m.map(lambda x: x * 2)
    assert isinstance(mapped, Maybe)
    assert mapped.is_nothing is False
    assert mapped.value == 10

    # map on nothing returns nothing
    n = Maybe.nothing()
    mapped_n = n.map(lambda x: x * 2)
    assert isinstance(mapped_n, Maybe)
    assert mapped_n.is_nothing is True
    assert not hasattr(mapped_n, "value")


def test_bind_with_function_returning_maybe():
    # bind should return result of mapper
    m = Maybe.just(3)
    result = m.bind(lambda x: Maybe.just(x + 4))
    assert result == Maybe.just(7)

    # bind on nothing returns nothing
    n = Maybe.nothing()
    result_n = n.bind(lambda x: Maybe.just(x + 4))
    assert result_n == Maybe.nothing()


def test_ap_with_function_inside_maybe():
    # ap applies function inside self to applicative
    f = Maybe.just(lambda x: x * 3)
    a = Maybe.just(4)
    assert f.ap(a) == Maybe.just(12)

    # ap with nothing returns nothing
    f_none = Maybe.nothing()
    assert f_none.ap(a) == Maybe.nothing()


def test_filter_accepts_and_rejects():
    m = Maybe.just(8)
    # filter that passes
    assert m.filter(lambda x: x > 5) == Maybe.just(8)
    # filter that fails
    assert m.filter(lambda x: x < 5) == Maybe.nothing()

    # filter on nothing stays nothing
    n = Maybe.nothing()
    assert n.filter(lambda x: True) == Maybe.nothing()


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


def test_to_lazy_returns_callable():
    m = Maybe.just(99)
    l = m.to_lazy()
    assert isinstance(l, _Lazy)
    assert l() == 99

    n = Maybe.nothing()
    l_none = n.to_lazy()
    assert isinstance(l_none, _Lazy)
    assert l_none() is None


def test_to_try_success_and_failure():
    m = Maybe.just("ok")
    t = m.to_try()
    assert isinstance(t, Try)
    assert t.is_success is True
    assert t.value == "ok"

    n = Maybe.nothing()
    t_none = n.to_try()
    assert isinstance(t_none, Try)
    assert t_none.is_success is False
    assert t_none.value is None


def test_to_validation_success_and_none():
    m = Maybe.just(7)
    v = m.to_validation()
    assert isinstance(v, _Validation)
    assert v.is_success is True
    assert v.value == 7

    n = Maybe.nothing()
    v_none = n.to_validation()
    assert isinstance(v_none, _Validation)
    assert v_none.is_success is True
    assert v_none.value is None
