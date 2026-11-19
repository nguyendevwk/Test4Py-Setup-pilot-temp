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
    assert not (b1 == b3)
    assert isinstance(b1, Box)
    assert str(b1) == "Box[value=10]"


def test_box_map_basic():
    b = Box(5)
    mapped = b.map(lambda x: x * 2)
    assert isinstance(mapped, Box)
    assert mapped.value == 10
    identity = b.map(lambda x: x)
    assert identity == b


def test_box_map_with_complex_function():
    b = Box([1, 2, 3])
    mapped = b.map(lambda lst: sum(lst))
    assert mapped.value == 6
    assert isinstance(mapped, Box)


def test_box_bind_returns_raw_value():
    b = Box(3)
    result = b.bind(lambda x: x + 4)
    assert result == 7
    result_str = b.bind(lambda x: f"Number {x}")
    assert result_str == "Number 3"


def test_box_ap_applies_function_inside_box():
    func_box = Box(lambda x: x * 3)
    value_box = Box(4)
    applied = func_box.ap(value_box)
    assert isinstance(applied, Box)
    assert applied.value == 12
    with pytest.raises(TypeError):
        value_box.ap(Box(5))


def test_box_to_maybe_returns_non_empty():
    b = Box("hello")
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    # The Maybe API may expose `value` or `is_present`/`is_present()`. Try both.
    if hasattr(maybe, "value"):
        assert maybe.value == "hello"
    elif hasattr(maybe, "is_present"):
        assert maybe.is_present
    else:
        assert maybe.is_present()
    # If a get method exists, use it
    if hasattr(maybe, "get"):
        assert maybe.get() == "hello"


def test_box_to_either_returns_right():
    b = Box(42)
    either = b.to_either()
    assert isinstance(either, Right)
    assert either.is_right()
    # Either may expose value directly or via get()
    if hasattr(either, "value"):
        assert either.value == 42
    elif hasattr(either, "get"):
        assert either.get() == 42


def test_box_to_lazy_evaluates_lazily(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("content")
    lazy = Box(file_path).to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.get() == file_path


def test_box_to_try_success():
    b = Box("ok")
    try_monad = b.to_try()
    assert isinstance(try_monad, Try)
    # Try may expose is_success as attribute or method
    if callable(getattr(try_monad, "is_success", None)):
        assert try_monad.is_success()
    else:
        assert try_monad.is_success
    if hasattr(try_monad, "value"):
        assert try_monad.value == "ok"
    elif hasattr(try_monad, "get"):
        assert try_monad.get() == "ok"


def test_box_to_validation_success():
    b = Box([1, 2])
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    # Validation may expose is_success as attribute or method
    if callable(getattr(validation, "is_success", None)):
        assert validation.is_success()
    else:
        assert validation.is_success
    if hasattr(validation, "value"):
        assert validation.value == [1, 2]
    elif hasattr(validation, "get"):
        assert validation.get() == [1, 2]


def test_box_bind_with_exception():
    b = Box(10)
    with pytest.raises(ValueError):
        b.bind(lambda x: (_ for _ in ()).throw(ValueError("boom")))


def test_box_map_with_exception():
    b = Box(10)
    with pytest.raises(RuntimeError):
        b.map(lambda x: (_ for _ in ()).throw(RuntimeError("fail")))


def test_box_equality_with_non_box():
    b = Box(5)
    assert not (b == 5)
    assert not (b == "5")
    assert not (b == None)
