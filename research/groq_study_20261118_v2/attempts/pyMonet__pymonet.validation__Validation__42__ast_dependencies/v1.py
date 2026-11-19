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
    v4 = Validation.fail(["err"])
    v5 = Validation.fail(["err"])
    v6 = Validation.fail(["other"])

    assert v1.is_success()
    assert not v1.is_fail()
    assert v1.value == 10
    assert v1.errors == []

    assert v4.is_fail()
    assert not v4.is_success()
    assert v4.value is None
    assert v4.errors == ["err"]

    assert v1 == v2
    assert v1 != v3
    assert v4 == v5
    assert v4 != v6


def test_map_on_success_and_fail():
    v = Validation.success(5)
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 10
    assert mapped.errors == []

    v_fail = Validation.fail(["e"])
    with pytest.raises(TypeError):
        v_fail.map(lambda x: x * 2)


def test_bind_returns_new_validation():
    def folder(x):
        return Validation.success(x + 1)

    v = Validation.success(3)
    bound = v.bind(folder)
    assert bound.value == 4
    assert bound.errors == []

    def folder_fail(x):
        return Validation.fail(["bad"])

    bound_fail = v.bind(folder_fail)
    assert bound_fail.value is None
    assert bound_fail.errors == ["bad"]


def test_ap_concatenates_errors_and_keeps_value():
    v = Validation.success(7)
    def fn(x):
        return Validation.fail(["err1", "err2"])
    result = v.ap(fn)
    assert result.value == 7
    assert result.errors == ["err1", "err2"]

    v2 = Validation.fail(["existing"])
    result2 = v2.ap(fn)
    assert result2.value is None
    assert result2.errors == ["existing", "err1", "err2"]


def test_to_either_success_and_failure():
    v = Validation.success("ok")
    either = v.to_either()
    assert isinstance(either, Right)
    assert either.value == "ok"

    v_fail = Validation.fail(["a", "b"])
    either_fail = v_fail.to_either()
    assert isinstance(either_fail, Left)
    assert either_fail.value == ["a", "b"]


def test_to_maybe_success_and_failure():
    v = Validation.success(42)
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    # The Maybe implementation does not expose an `is_present` method.
    # Instead we check the presence of a value via its truthiness.
    assert maybe.value == 42

    v_fail = Validation.fail(["err"])
    maybe_fail = v_fail.to_maybe()
    assert isinstance(maybe_fail, Maybe)
    assert maybe_fail.value is None


def test_to_box_and_to_lazy_and_to_try():
    v = Validation.success("data")
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "data"

    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    # Lazy exposes the computed value via the `value` attribute.
    assert lazy.value == "data"

    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == "data"

    v_fail = Validation.fail(["err"])
    try_fail = v_fail.to_try()
    assert isinstance(try_fail, Try)
    assert not try_fail.is_success()
    assert try_fail.value is None


def test_str_representation():
    v = Validation.success(1)
    assert str(v) == "Validation.success[1]"

    v_fail = Validation.fail(["e"])
    assert str(v_fail) == "Validation.fail[None, ['e']]"
