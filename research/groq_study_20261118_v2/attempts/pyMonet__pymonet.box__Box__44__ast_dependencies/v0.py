import pytest
from pymonet.box import Box
from pymonet.maybe import Maybe
from pymonet.either import Right
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation


def test_equality_and_str():
    b1 = Box(10)
    b2 = Box(10)
    b3 = Box(20)
    assert b1 == b2
    assert b1 != b3
    assert isinstance(b1, Box)
    assert str(b1) == "Box[value=10]"


def test_map_transforms_value():
    b = Box(5)
    mapped = b.map(lambda x: x * 2)
    assert isinstance(mapped, Box)
    assert mapped.value == 10
    # original remains unchanged
    assert b.value == 5


def test_bind_returns_mapped_value():
    b = Box("hello")
    result = b.bind(lambda s: s.upper())
    assert result == "HELLO"
    # bind does not wrap in Box
    assert not isinstance(result, Box)


def test_ap_applies_function_inside_box():
    # Box containing a function
    func_box = Box(lambda x: x + 3)
    # Box containing a value
    val_box = Box(7)
    # ap should apply function to value
    result = val_box.ap(func_box)
    assert isinstance(result, Box)
    assert result.value == 10


def test_to_maybe_returns_non_empty():
    b = Box(42)
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_just()
    assert maybe.value == 42


def test_to_either_returns_right():
    b = Box("ok")
    either = b.to_either()
    assert isinstance(either, Right)
    assert either.value == "ok"


def test_to_lazy_returns_lazy_with_value():
    b = Box([1, 2, 3])
    lazy = b.to_lazy()
    assert isinstance(lazy, Lazy)
    # Lazy should not evaluate until called
    assert lazy.is_lazy()
    assert lazy() == [1, 2, 3]


def test_to_try_returns_successful_try():
    b = Box(3.14)
    t = b.to_try()
    assert isinstance(t, Try)
    assert t.is_success()
    assert t.value == 3.14


def test_to_validation_returns_successful_validation():
    b = Box({"key": "value"})
    v = b.to_validation()
    assert isinstance(v, Validation)
    assert v.is_success()
    assert v.value == {"key": "value"}


def test_map_with_exception_propagates():
    b = Box(5)
    with pytest.raises(ValueError):
        b.map(lambda x: (_ for _ in ()).throw(ValueError("boom")))


def test_bind_with_exception_propagates():
    b = Box(5)
    with pytest.raises(RuntimeError):
        b.bind(lambda x: (_ for _ in ()).throw(RuntimeError("oops")))


def test_ap_with_non_function_raises():
    b = Box(5)
    non_func_box = Box(10)
    with pytest.raises(TypeError):
        b.ap(non_func_box)


def test_to_maybe_with_none_value():
    b = Box(None)
    maybe = b.to_maybe()
    assert maybe.is_just()
    assert maybe.value is None


def test_to_either_with_none_value():
    b = Box(None)
    either = b.to_either()
    assert either.is_right()
    assert either.value is None


def test_to_lazy_with_callable():
    b = Box(lambda: 99)
    lazy = b.to_lazy()
    assert lazy() == 99


def test_to_try_with_exception_value():
    # Box can hold an exception object
    exc = ValueError("error")
    b = Box(exc)
    t = b.to_try()
    assert t.is_success()
    assert t.value is exc
