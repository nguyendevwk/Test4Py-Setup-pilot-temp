import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_either_conversion():
    val = Validation.success(42)
    assert val.is_success()
    assert val.is_fail() is False
    assert val.value == 42
    assert val.errors == []

    either = val.to_either()
    assert isinstance(either, Right)
    assert either.value == 42

    maybe = val.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.value == 42

    box = val.to_box()
    assert isinstance(box, Box)
    assert box.value == 42

    lazy = val.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.run() == 42

    try_monad = val.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == 42


def test_fail_and_bind_and_ap():
    errors = ["error1", "error2"]
    val = Validation.fail(errors)
    assert val.is_fail()
    assert val.is_success() is False
    assert val.value is None
    assert val.errors == errors

    # bind should propagate the failure unchanged
    def folder(x):
        return Validation.success(x + 1)
    bound = val.bind(folder)
    assert bound == val  # same failure

    # ap should concatenate errors
    def fn(x):
        return Validation.fail(["error3"])
    applied = val.ap(fn)
    assert applied.errors == errors + ["error3"]
    assert applied.value == val.value


def test_map_and_either_failure():
    val = Validation.success("hello")
    mapped = val.map(str.upper)
    assert mapped.value == "HELLO"
    assert mapped.errors == []

    # map on failure should keep errors
    fail_val = Validation.fail(["oops"])
    mapped_fail = fail_val.map(lambda x: x * 2)
    assert mapped_fail.errors == ["oops"]
    assert mapped_fail.value is None

    # to_either on failure returns Left
    left = fail_val.to_either()
    assert isinstance(left, Left)
    assert left.value == ["oops"]
