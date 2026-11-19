import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try

def test_success_and_either_conversion():
    v = Validation.success(42)
    assert v.is_success()
    assert v.is_fail() is False
    assert v.value == 42
    assert v.errors == []
    # to_either should produce Right
    either = v.to_either()
    assert isinstance(either, Right)
    assert either.value == 42
    # to_maybe should produce just
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.value == 42
    # to_box should wrap value
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == 42
    # to_lazy should return a Lazy that yields the value
    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.run() == 42
    # to_try should be successful
    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == 42

def test_fail_and_either_conversion():
    errors = ["error1", "error2"]
    v = Validation.fail(errors)
    assert v.is_fail()
    assert v.is_success() is False
    assert v.value is None
    assert v.errors == errors
    # to_either should produce Left
    either = v.to_either()
    assert isinstance(either, Left)
    assert either.value == errors
    # to_maybe should be nothing
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    assert not maybe.is_present()
    # to_try should be failure
    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert not try_monad.is_success()
    assert try_monad.value is None

def test_map_bind_ap_and_equality():
    v = Validation.success(3)
    # map should transform value
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 6
    assert mapped.errors == []
    # bind should apply function returning Validation
    bound = v.bind(lambda x: Validation.success(x + 1))
    assert bound.value == 4
    assert bound.errors == []
    # ap should concatenate errors from function Validation
    v2 = Validation.success(10)
    fn_val = Validation.success(lambda x: x + 5)
    ap_res = v2.ap(fn_val)
    assert ap_res.value == 10
    assert ap_res.errors == []
    # equality checks
    assert v == Validation.success(3)
    assert v != Validation.success(4)
    assert v != Validation.fail(["err"])
