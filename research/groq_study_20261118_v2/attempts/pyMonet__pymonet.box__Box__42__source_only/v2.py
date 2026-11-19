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
    assert str(b1) == "Box[value=10]"


def test_box_map_identity_and_transformation():
    b = Box(5)
    mapped = b.map(lambda x: x)
    assert isinstance(mapped, Box)
    assert mapped.value == 5
    mapped2 = b.map(lambda x: x * 2)
    assert mapped2.value == 10
    assert b.value == 5


def test_box_bind_returns_value():
    b = Box(3)
    result = b.bind(lambda x: x + 4)
    assert result == 7
    result_box = b.bind(lambda x: Box(x * 2))
    assert isinstance(result_box, Box)
    assert result_box.value == 6


def test_box_ap_applies_function_from_other_box():
    b = Box(4)
    func_box = Box(lambda x: x + 1)
    applied = func_box.ap(b)
    assert isinstance(applied, Box)
    assert applied.value == 5
    with pytest.raises(TypeError):
        b.ap(Box(10))


def test_box_to_maybe_returns_non_empty():
    b = Box("hello")
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    assert getattr(maybe, "is_some", lambda: False)()
    assert getattr(maybe, "get_value", lambda: None)() == "hello"


def test_box_to_either_returns_right():
    b = Box(42)
    either = b.to_either()
    assert isinstance(either, Right)
    assert getattr(either, "is_right", lambda: False)()
    assert either.value == 42


def test_box_to_lazy_returns_lazy_with_correct_value(tmp_path):
    b = Box("lazy")
    lazy = b.to_lazy()
    assert isinstance(lazy, Lazy)
    assert getattr(lazy, "is_evaluated", lambda: True)() is False
    assert getattr(lazy, "get_value", lambda: None)() == "lazy"
    assert getattr(lazy, "get_value", lambda: None)() == "lazy"


def test_box_to_try_returns_successful_try():
    b = Box([1, 2, 3])
    try_obj = b.to_try()
    assert isinstance(try_obj, Try)
    assert try_obj.is_success
    assert try_obj.get_value() == [1, 2, 3]


def test_box_to_validation_returns_successful_validation():
    b = Box({"key": "value"})
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    assert validation.is_success
    assert getattr(validation, "get_value", lambda: None)() == {"key": "value"}


def test_box_map_with_exception_propagates():
    b = Box(10)
    with pytest.raises(ValueError):
        b.map(lambda x: (_ for _ in ()).throw(ValueError("boom")))


def test_box_bind_with_exception_propagates():
    b = Box(10)
    with pytest.raises(RuntimeError):
        b.bind(lambda x: (_ for _ in ()).throw(RuntimeError("error")))


def test_box_ap_with_non_box_raises_type_error():
    b = Box(5)
    with pytest.raises(TypeError):
        b.ap(5)


def test_box_equality_with_non_box_returns_false():
    b = Box(5)
    assert (b == 5) is False
    assert (b == "5") is False
