import pytest
from pymonet.box import Box
from pymonet.maybe import Maybe
from pymonet.either import Right
from pymonet.lazy import Lazy
from pymonet.monad_try import Try
from pymonet.validation import Validation


def test_box_map_and_equality():
    """Test that map transforms the value and equality compares wrapped values."""
    b1 = Box(10)
    b2 = Box(10)
    b3 = Box(20)

    # Equality should be based on the wrapped value
    assert b1 == b2
    assert b1 != b3

    # map should apply the function and return a new Box
    b4 = b1.map(lambda x: x * 2)
    assert isinstance(b4, Box)
    assert b4.value == 20
    # original box remains unchanged
    assert b1.value == 10


def test_box_bind_and_ap():
    """Test bind returns the function result and ap applies function from another Box."""
    b = Box(5)

    # bind should apply the function and return its result directly
    result = b.bind(lambda x: x + 3)
    assert result == 8

    # ap should apply the function inside the Box to another Box
    func_box = Box(lambda x: x * 4)
    applied = b.ap(func_box)
    assert isinstance(applied, Box)
    assert applied.value == 20


def test_box_conversions(tmp_path):
    """Test conversions to other monads preserve the value."""
    value = "hello"
    b = Box(value)

    # to_maybe should produce a non-empty Maybe
    maybe = b.to_maybe()
    assert isinstance(maybe, Maybe)
    assert maybe.is_present()
    assert maybe.get() == value

    # to_either should produce a Right
    either = b.to_either()
    assert isinstance(either, Right)
    assert either.get() == value

    # to_lazy should produce a Lazy that returns the value
    lazy = b.to_lazy()
    assert isinstance(lazy, Lazy)
    assert lazy.get() == value

    # to_try should produce a successful Try
    try_monad = b.to_try()
    assert isinstance(try_monad, Try)
    assert try_monad.is_success()
    assert try_monad.get() == value

    # to_validation should produce a successful Validation
    validation = b.to_validation()
    assert isinstance(validation, Validation)
    assert validation.is_success()
    assert validation.get() == value
