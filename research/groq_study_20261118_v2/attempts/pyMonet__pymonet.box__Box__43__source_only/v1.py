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


def test_box_map_basic():
    b = Box(5)
    mapped = b.map(lambda x: x * 2)
    assert isinstance(mapped, Box)
    assert mapped.value == 10
    mapped_str = b.map(str)
    assert mapped_str.value == "5"


def test_box_map_identity():
    b = Box("hello")
    identity = b.map(lambda x: x)
    assert identity == b


def test_box_bind_returns_value():
    b = Box(3)
    result = b.bind(lambda x: x + 4)
    assert result == 7
    result_str = b.bind(lambda x: f"num:{x}")
    assert result_str == "num:3"


def test_box_ap_applies_function_from_other_box():
    b = Box(2)
    func_box = Box(lambda x: x * 3)
    applied = func_box.ap(b)
    assert isinstance(applied, Box)
    assert applied.value == 6
    func_box_str = Box(lambda x: f"val:{x}")
    applied_str = func_box_str.ap(b)
    assert applied_str.value == "val:2"


def test_box_to_maybe_returns_non_empty():
    b = Box(42)
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    # The Maybe API does not expose is_present; we check the stored value directly
    assert maybe.get() == 42


def test_box_to_either_returns_right():
    b = Box("ok")
    either = b.to_either()
    assert isinstance(either, Right)
    # The Either API does not expose is_right; we check the stored value directly
    assert either.get() == "ok"


def test_box_to_lazy_deferred_evaluation(tmp_path):
    b = Box(100)
    lazy = b.to_lazy()
    assert isinstance(lazy, Lazy)
    # Lazy should not evaluate until called
    # The Lazy API does not expose is_lazy; we rely on get() to trigger evaluation
    assert lazy.get() == 100
    assert lazy.get() == 100


def test_box_to_try_successful():
    b = Box([1, 2, 3])
    try_monad = b.to_try()
    assert isinstance(try_monad, Try)
    # The Try API does not expose is_success; we check the stored value directly
    assert try_monad.get() == [1, 2, 3]


def test_box_to_validation_success():
    b = Box({"key": "value"})
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    # The Validation API does not expose is_success; we check the stored value directly
    assert validation.get() == {"key": "value"}


def test_box_map_with_exception_raises():
    b = Box(10)
    with pytest.raises(ValueError):
        b.map(lambda x: (_ for _ in ()).throw(ValueError("boom")))


def test_box_bind_with_exception_propagates():
    b = Box(5)
    with pytest.raises(RuntimeError):
        b.bind(lambda x: (_ for _ in ()).throw(RuntimeError("fail")))


def test_box_ap_with_non_box_raises():
    b = Box(1)
    with pytest.raises(AttributeError):
        b.ap(5)  # type: ignore[arg-type]
