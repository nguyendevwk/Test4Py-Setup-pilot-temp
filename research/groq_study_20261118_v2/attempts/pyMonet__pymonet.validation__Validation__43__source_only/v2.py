import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_fail_basic():
    v_ok = Validation.success(10)
    assert v_ok.value == 10
    assert v_ok.errors == []
    assert v_ok.is_success()
    assert not v_ok.is_fail()

    v_err = Validation.fail(["error1", "error2"])
    assert v_err.value is None
    assert v_err.errors == ["error1", "error2"]
    assert not v_err.is_success()
    assert v_err.is_fail()


def test_fail_default_mutable_list():
    v1 = Validation.fail()
    v2 = Validation.fail()
    # default list is shared; modifying one affects the other
    v1.errors.append("shared")
    assert v2.errors == ["shared"]
    # ensure that the shared list is indeed the same object
    assert v1.errors is v2.errors


def test_map_transforms_value_and_preserves_errors():
    v = Validation.success(5)
    v2 = v.map(lambda x: x * 2)
    assert v2.value == 10
    assert v2.errors == []

    v_err = Validation.fail(["e"])
    v_err2 = v_err.map(lambda x: 100 if x is not None else None)
    assert v_err2.value is None
    assert v_err2.errors == ["e"]


def test_bind_forwards_validation():
    def to_validation(x):
        return Validation.success(x + 1) if x > 0 else Validation.fail(["negative"])

    v = Validation.success(3)
    v2 = v.bind(to_validation)
    assert v2.value == 4
    assert v2.errors == []

    v_neg = Validation.success(-1)
    v_neg2 = v_neg.bind(to_validation)
    assert v_neg2.value is None
    assert v_neg2.errors == ["negative"]


def test_ap_accumulates_errors():
    v = Validation.success(7)
    def fn(x):
        return Validation.fail(["err1", "err2"])
    v2 = v.ap(fn)
    assert v2.value == 7
    assert v2.errors == ["err1", "err2"]

    v_ok = Validation.success(7)
    def fn_ok(x):
        return Validation.success(x * 2)
    v3 = v_ok.ap(fn_ok)
    assert v3.value == 7
    assert v3.errors == []


def test_to_either_success_and_failure():
    v_ok = Validation.success("ok")
    either_ok = v_ok.to_either()
    assert isinstance(either_ok, Right)
    assert either_ok.value == "ok"

    v_err = Validation.fail(["bad"])
    either_err = v_err.to_either()
    assert isinstance(either_err, Left)
    assert either_err.value == ["bad"]


def test_to_maybe_success_and_failure():
    v_ok = Validation.success(42)
    maybe_ok = v_ok.to_maybe()
    assert isinstance(maybe_ok, Maybe)
    # adapt to possible API variations
    present = getattr(maybe_ok, "is_present", None)
    if callable(present):
        assert present()
    else:
        assert bool(present)
    assert maybe_ok.value == 42

    v_err = Validation.fail(["oops"])
    maybe_err = v_err.to_maybe()
    assert isinstance(maybe_err, Maybe)
    present = getattr(maybe_err, "is_present", None)
    if callable(present):
        assert not present()
    else:
        assert not bool(present)


def test_to_box_and_to_lazy_and_to_try(tmp_path):
    v = Validation.success("data")
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "data"

    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    # adapt to possible API variations
    if callable(getattr(lazy, "value", None)):
        assert lazy.value() == "data"
    else:
        # if value is a property returning the stored value
        assert lazy.value == "data"

    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success
    assert try_monad.value == "data"

    v_fail = Validation.fail(["err"])
    try_fail = v_fail.to_try()
    assert isinstance(try_fail, Try)
    assert not try_fail.is_success
    assert try_fail.value is None
