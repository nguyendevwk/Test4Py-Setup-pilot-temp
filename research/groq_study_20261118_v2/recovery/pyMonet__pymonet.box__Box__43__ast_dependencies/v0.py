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
    mapped = b.map(lambda x: x * 2)
    assert isinstance(mapped, Box)
    assert mapped.value == 10
    # mapping to a different type
    mapped_str = b.map(str)
    assert mapped_str.value == "5"


def test_bind_returns_mapped_value():
    b = Box(3)
    result = b.bind(lambda x: x + 4)
    assert result == 7
    # bind can return any type
    result_tuple = b.bind(lambda x: (x, x * 2))
    assert result_tuple == (3, 6)


def test_ap_applies_function_from_other_box():
    b = Box(4)
    func_box = Box(lambda x: x + 1)
    applied = b.ap(func_box)
    assert isinstance(applied, Box)
    assert applied.value == 5


def test_to_maybe_returns_non_empty_maybe():
    b = Box("hello")
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.get() == "hello"


def test_to_either_returns_right():
    b = Box(42)
    either = b.to_either()
    assert isinstance(either, Right)
    assert either.get() == 42


def test_to_lazy_returns_lazy_with_value():
    b = Box([1, 2, 3])
    lazy = b.to_lazy()
    assert isinstance(lazy, Lazy)
    # Lazy should not evaluate until called
    assert lazy.is_lazy()
    assert lazy.get() == [1, 2, 3]


def test_to_try_returns_successful_try():
    b = Box("ok")
    try_monad = b.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.get() == "ok"


def test_to_validation_returns_successful_validation():
    b = Box(99)
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    assert validation.is_success()
    assert validation.get() == 99


def test_map_with_non_callable_raises_type_error():
    b = Box(1)
    with pytest.raises(TypeError):
        b.map(42)  # type: ignore[arg-type]


def test_bind_with_non_callable_raises_type_error():
    b = Box(1)
    with pytest.raises(TypeError):
        b.bind(42)  # type: ignore[arg-type]


def test_ap_with_non_box_raises_attribute_error():
    b = Box(1)
    with pytest.raises(AttributeError):
        b.ap(5)  # type: ignore[arg-type]


def test_equality_with_non_box_returns_false():
    b = Box(1)
    assert (b == 1) is False
    assert (b == "1") is False
