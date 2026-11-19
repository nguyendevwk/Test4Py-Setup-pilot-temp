import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_fail_and_equality():
    v1 = Validation.success(10)
    v2 = Validation.success(10)
    v3 = Validation.success(20)
    v4 = Validation.fail([1, 2])
    v5 = Validation.fail([1, 2])
    v6 = Validation.fail([2, 1])

    assert v1.is_success()
    assert not v1.is_fail()
    assert v4.is_fail()
    assert not v4.is_success()

    assert v1 == v2
    assert v1 != v3
    assert v4 == v5
    assert v4 != v6  # order matters in list comparison


def test_map_and_bind():
    v = Validation.success(5)
    mapped = v.map(lambda x: x * 2)
    assert mapped.value == 10
    assert mapped.errors == []

    # bind should return a new Validation
    bound = v.bind(lambda x: Validation.success(x + 3))
    assert bound.value == 8
    assert bound.errors == []

    # bind with failure propagates errors
    bound_fail = v.bind(lambda x: Validation.fail(["error"]))
    assert bound_fail.is_fail()
    assert bound_fail.errors == ["error"]
    assert bound_fail.value is None


def test_ap_concatenates_errors_and_keeps_value():
    v = Validation.success("hello")
    fn = lambda x: Validation.fail(["err1", "err2"])
    result = v.ap(fn)
    assert result.value == "hello"
    assert result.errors == ["err1", "err2"]

    # multiple calls accumulate errors
    fn2 = lambda x: Validation.fail(["err3"])
    result2 = result.ap(fn2)
    assert result2.errors == ["err1", "err2", "err3"]


def test_to_either_success_and_failure():
    v_ok = Validation.success("ok")
    either_ok = v_ok.to_either()
    assert isinstance(either_ok, Right)
    assert either_ok.value == "ok"

    v_err = Validation.fail(["e1", "e2"])
    either_err = v_err.to_either()
    assert isinstance(either_err, Left)
    assert either_err.value == ["e1", "e2"]


def test_to_maybe_success_and_failure():
    v_ok = Validation.success(42)
    maybe_ok = v_ok.to_maybe()
    assert isinstance(maybe_ok, Maybe)
    assert maybe_ok.is_present()
    assert maybe_ok.value == 42

    v_err = Validation.fail(["oops"])
    maybe_err = v_err.to_maybe()
    assert isinstance(maybe_err, Maybe)
    assert not maybe_err.is_present()


def test_to_box_and_to_lazy_and_to_try():
    v = Validation.success("data")
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == "data"

    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.run() == "data"

    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == "data"

    # failure case for Try
    v_fail = Validation.fail(["err"])
    try_fail = v_fail.to_try()
    assert isinstance(try_fail, Try)
    assert not try_fail.is_success()
    assert try_fail.value is None


def test_fail_default_mutable_list_shared():
    # The default argument for fail is a mutable list; ensure that
    # modifying one instance's errors affects others if they share the list.
    v1 = Validation.fail()
    v2 = Validation.fail()
    v1.errors.append("shared")
    assert "shared" in v2.errors
    # Ensure that explicit list creates independent copies
    v3 = Validation.fail(["explicit"])
    v4 = Validation.fail(["explicit"])
    v3.errors.append("changed")
    assert "changed" not in v4.errors
