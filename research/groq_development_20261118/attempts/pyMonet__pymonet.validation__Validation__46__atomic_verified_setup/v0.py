import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try

def test_success_and_map_and_bind():
    # Create a successful Validation and test map and bind operations
    v = Validation.success(10)
    assert v.is_success()
    assert v.is_fail() is False
    # map should apply function to value and keep errors unchanged
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 20
    assert mapped.errors == []
    # bind should apply a function that returns a Validation
    bound = v.bind(lambda x: Validation.success(x + 5))
    assert bound.value == 15
    assert bound.errors == []

def test_fail_and_ap_and_to_either():
    # Create a failed Validation with multiple errors
    v = Validation.fail(["err1", "err2"])
    assert v.is_fail()
    assert v.is_success() is False
    # ap should concatenate errors from function Validation
    def fn(val):
        return Validation.fail(["err3"])
    aped = v.ap(fn)
    assert aped.value == v.value  # value unchanged
    assert aped.errors == ["err1", "err2", "err3"]
    # to_either should produce a Left with errors
    either = v.to_either()
    assert isinstance(either, Left)
    assert either.value == ["err1", "err2"]

def test_to_maybe_box_lazy_try_and_equality():
    # Successful Validation should convert to Maybe.just, Box, Lazy, Try
    v = Validation.success("ok")
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.value == "ok"

    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "ok"

    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.value() == "ok"

    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == "ok"

    # Equality: two validations with same value and errors are equal
    v2 = Validation.success("ok")
    assert v == v2
    # Different errors make them unequal
    v3 = Validation.success("ok")
    v3.errors.append("extra")
    assert v != v3
