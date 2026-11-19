import pytest
from pymonet.box import Box
from pymonet.maybe import Maybe
from pymonet.either import Right
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation


def test_box_equality_and_str():
    b1 = Box(10)
    b2 = Box(10)
    b3 = Box(20)
    assert b1 == b2
    assert b1 != b3
    assert isinstance(b1, Box)
    assert str(b1) == "Box[value=10]"


def test_map_transforms_value():
    b = Box(5)
    b2 = b.map(lambda x: x * 2)
    assert isinstance(b2, Box)
    assert b2.value == 10
    assert b.value == 5


def test_bind_returns_mapped_value():
    b = Box("hello")
    result = b.bind(lambda s: s.upper())
    assert result == "HELLO"
    assert not isinstance(result, Box)


def test_ap_applies_function_from_other_box():
    func_box = Box(lambda x: x + 3)
    val_box = Box(7)
    result = func_box.ap(val_box)
    assert isinstance(result, Box)
    assert result.value == 10


def test_to_maybe_returns_non_empty_maybe():
    b = Box(42)
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
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
    assert lazy.value == [1, 2, 3]


def test_to_try_returns_successful_try():
    b = Box(3.14)
    try_monad = b.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success
    assert try_monad.value == 3.14


def test_to_validation_returns_successful_validation():
    b = Box({"key": "value"})
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    assert validation.is_success
    assert validation.value == {"key": "value"}


def test_map_with_non_callable_raises_type_error():
    b = Box(1)
    with pytest.raises(TypeError):
        b.map(42)  # type: ignore[arg-type]


def test_bind_with_non_callable_raises_type_error():
    b = Box(1)
    with pytest.raises(TypeError):
        b.bind(42)  # type: ignore[arg-type]


def test_ap_with_non_box_raises_attribute_error():
    b = Box(5)
    with pytest.raises(AttributeError):
        b.ap(5)  # type: ignore[arg-type]
