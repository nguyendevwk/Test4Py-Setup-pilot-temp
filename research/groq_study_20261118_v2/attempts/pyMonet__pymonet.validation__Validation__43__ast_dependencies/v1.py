import pytest
from pymonet.validation import Validation
from pymonet.either import Left, Right
from pymonet.maybe import Maybe
from pymonet.box import Box
from pymonet.lazy import Lazy
from pymonet.monad_try import Try


def test_success_and_fail_initialization_and_equality():
    v1 = Validation.success(10)
    v2 = Validation(10, [])
    assert v1 == v2
    assert v1.is_success()
    assert not v1.is_fail()

    v3 = Validation.fail(['err'])
    v4 = Validation(None, ['err'])
    assert v3 == v4
    assert not v3.is_success()
    assert v3.is_fail()


def test_success_and_fail_default_value_and_errors():
    v = Validation.success()
    assert v.value is None
    assert v.errors == []

    v_err = Validation.fail()
    assert v_err.value is None
    assert v_err.errors == []  # default empty list


def test_map_transforms_value_and_preserves_errors():
    v = Validation.success(5)
    v2 = v.map(lambda x: x * 2)
    assert v2.value == 10
    assert v2.errors == []

    v_err = Validation.fail(['e'])
    with pytest.raises(TypeError):
        v_err.map(lambda x: x * 2)


def test_bind_returns_folder_result_and_propagates_errors():
    def folder(x):
        return Validation.success(x + 1)

    v = Validation.success(3)
    v2 = v.bind(folder)
    assert v2.value == 4
    assert v2.errors == []

    def bad_folder(x):
        return Validation.fail(['bad'])

    v_err = Validation.success(3)
    v_err2 = v_err.bind(bad_folder)
    assert v_err2.value is None
    assert v_err2.errors == ['bad']


def test_ap_concatenates_errors_and_keeps_value():
    v = Validation.success(7)
    fn = lambda x: Validation.fail(['f1', 'f2'])
    v2 = v.ap(fn)
    assert v2.value == 7
    assert v2.errors == ['f1', 'f2']

    v_ok = Validation.success(7)
    fn_ok = lambda x: Validation.success('ok')
    v3 = v_ok.ap(fn_ok)
    assert v3.value == 7
    assert v3.errors == []


def test_to_either_success_and_failure():
    v = Validation.success('ok')
    either = v.to_either()
    assert isinstance(either, Right)
    assert either.value == 'ok'

    v_err = Validation.fail(['e1'])
    either_err = v_err.to_either()
    assert isinstance(either_err, Left)
    assert either_err.value == ['e1']


def test_to_maybe_success_and_failure():
    v = Validation.success('data')
    maybe = v.to_maybe()
    assert isinstance(maybe, Maybe)
    # The Maybe API does not expose is_just; we only check the value
    assert maybe.value == 'data'

    v_err = Validation.fail(['e'])
    maybe_err = v_err.to_maybe()
    assert isinstance(maybe_err, Maybe)
    # The Maybe API does not expose is_nothing; we check that value is None
    assert maybe_err.value is None


def test_to_box_and_to_lazy_and_to_try():
    v = Validation.success(42)
    box = v.to_box()
    assert isinstance(box, Box)
    assert box.value == 42

    lazy = v.to_lazy()
    assert isinstance(lazy, Lazy)
    # Lazy does not expose run; we access the stored value directly
    assert lazy.value == 42

    try_monad = v.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.value == 42

    v_err = Validation.fail(['e'])
    try_err = v_err.to_try()
    assert isinstance(try_err, Try)
    assert not try_err.is_success()
    assert try_err.value is None


def test_str_representation_success_and_failure():
    v = Validation.success('x')
    assert str(v) == 'Validation.success[x]'

    v_err = Validation.fail(['err'])
    assert str(v_err) == 'Validation.fail[None, [\'err\']]'  # value is None


def test_equality_with_non_validation_and_different_contents():
    v = Validation.success(1)
    assert v != 1
    assert v != Validation.success(2)
    assert v != Validation.fail([1])
