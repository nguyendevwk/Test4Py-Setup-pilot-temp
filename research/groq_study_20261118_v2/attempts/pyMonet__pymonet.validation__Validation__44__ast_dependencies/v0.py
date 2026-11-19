import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_fail_initialization_and_equality():
    v1 = Validation.success(10)
    v2 = Validation.success(10)
    v3 = Validation.success(20)
    v4 = Validation.fail(["error"])

    assert v1.is_success()
    assert not v1.is_fail()
    assert v1.value == 10
    assert v1.errors == []

    assert v4.is_fail()
    assert not v4.is_success()
    assert v4.value is None
    assert v4.errors == ["error"]

    assert v1 == v2
    assert v1 != v3
    assert v1 != v4


def test_map_transforms_value_and_preserves_errors():
    v = Validation.success(5)
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 10
    assert mapped.errors == []

    v_fail = Validation.fail(["err"])
    mapped_fail = v_fail.map(lambda x: x * 2)
    assert mapped_fail.value is None
    assert mapped_fail.errors == ["err"]


def test_bind_returns_folder_result_and_propagates_errors():
    def folder(x):
        return Validation.success(x + 1)

    v = Validation.success(3)
    bound = v.bind(folder)
    assert bound.value == 4
    assert bound.errors == []

    def bad_folder(x):
        return Validation.fail(["bad"])

    bound_fail = v.bind(bad_folder)
    assert bound_fail.value is None
    assert bound_fail.errors == ["bad"]


def test_ap_concatenates_errors_and_keeps_value():
    v = Validation.success(7)
    fn = lambda x: Validation.fail(["e1", "e2"])
    result = v.ap(fn)
    assert result.value == 7
    assert result.errors == ["e1", "e2"]

    v2 = Validation.fail(["e0"])
    result2 = v2.ap(fn)
    assert result2.value is None
    assert result2.errors == ["e0", "e1", "e2"]


def test_to_either_converts_success_and_failure():
    v = Validation.success("ok")
    either = v.to_either()
    assert isinstance(either, Right)
    assert either.value == "ok"

    v_fail = Validation.fail(["oops"])
    either_fail = v_fail.to_either()
    assert isinstance(either_fail, Left)
    assert either_fail.value == ["oops"]


def test_to_maybe_converts_success_and_failure():
    v = Validation.success(42)
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.value == 42

    v_fail = Validation.fail(["none"])
    maybe_fail = v_fail.to_maybe()
    assert isinstance(maybe_fail, Maybe)
    assert not maybe_fail.is_present()


def test_to_box_returns_box_with_value():
    v = Validation.success("data")
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "data"

    v_fail = Validation.fail(["err"])
    box_fail = v_fail.to_box()
    assert isinstance(box_fail, Box)
    assert box_fail.value is None


def test_to_lazy_returns_lazy_evaluating_value():
    v = Validation.success(99)
    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.evaluate() == 99

    v_fail = Validation.fail(["err"])
    lazy_fail = v_fail.to_lazy()
    assert lazy_fail.evaluate() is None


def test_to_try_returns_success_or_failure_based_on_errors():
    v = Validation.success("ok")
    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == "ok"

    v_fail = Validation.fail(["bad"])
    try_fail = v_fail.to_try()
    assert isinstance(try_fail, Try)
    assert not try_fail.is_success()
    assert try_fail.value is None
