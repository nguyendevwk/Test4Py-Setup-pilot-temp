import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_fail_value_and_errors():
    v = Validation.success(10)
    assert v.value == 10
    assert v.errors == []
    assert v.is_success()
    assert not v.is_fail()

    f = Validation.fail(["err1", "err2"])
    assert f.value is None
    assert f.errors == ["err1", "err2"]
    assert not f.is_success()
    assert f.is_fail()


def test_fail_default_list_is_shared():
    f1 = Validation.fail()
    f2 = Validation.fail()
    f1.errors.append("shared")
    assert f2.errors == ["shared"]  # default list is shared


def test_map_transforms_value_and_preserves_errors():
    v = Validation.success(5)
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 10
    assert mapped.errors == []

    f = Validation.fail(["e"])
    mapped_fail = f.map(lambda x: x * 2)
    assert mapped_fail.value is None
    assert mapped_fail.errors == ["e"]


def test_bind_returns_folder_result_and_discards_original_value():
    v = Validation.success(3)
    result = v.bind(lambda x: Validation.success(x + 4))
    assert result.value == 7
    assert result.errors == []

    f = Validation.fail(["e"])
    result_fail = f.bind(lambda x: Validation.success(x + 4))
    assert result_fail.value is None
    assert result_fail.errors == ["e"]


def test_ap_concatenates_errors_and_keeps_value():
    v = Validation.success(2)
    fn = lambda x: Validation.fail(["f1", "f2"])
    combined = v.ap(fn)
    assert combined.value == 2
    assert combined.errors == ["f1", "f2"]

    v2 = Validation.success(3)
    fn2 = lambda x: Validation.success(x * 10)
    combined2 = v2.ap(fn2)
    assert combined2.value == 3
    assert combined2.errors == []


def test_to_either_success_and_failure():
    v = Validation.success("ok")
    either = v.to_either()
    assert isinstance(either, Right)
    assert either.value == "ok"

    f = Validation.fail(["err"])
    either_fail = f.to_either()
    assert isinstance(either_fail, Left)
    assert either_fail.value == ["err"]


def test_to_maybe_success_and_failure():
    v = Validation.success(42)
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.value == 42

    f = Validation.fail(["err"])
    maybe_fail = f.to_maybe()
    assert isinstance(maybe_fail, Maybe)
    assert not maybe_fail.is_present()


def test_to_box_returns_box_with_value():
    v = Validation.success("data")
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "data"

    f = Validation.fail(["err"])
    box_fail = f.to_box()
    assert isinstance(box_fail, Box)
    assert box_fail.value is None


def test_to_lazy_returns_lazy_evaluating_value():
    v = Validation.success(99)
    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.run() == 99

    f = Validation.fail(["err"])
    lazy_fail = f.to_lazy()
    assert isinstance(lazy_fail, Lazy)
    assert lazy_fail.run() is None


def test_to_try_success_and_failure(tmp_path):
    v = Validation.success("ok")
    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == "ok"

    f = Validation.fail(["err"])
    try_fail = f.to_try()
    assert isinstance(try_fail, Try)
    assert not try_fail.is_success()
    assert try_fail.value is None
