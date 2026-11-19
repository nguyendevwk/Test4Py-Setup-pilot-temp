import pytest
from pymonet.box import Box

def test_box_map_and_equality():
    # Create a Box containing an integer
    b1 = Box(10)
    # Map a function over the Box
    b2 = b1.map(lambda x: x * 2)
    # The result should be a new Box with the mapped value
    assert isinstance(b2, Box)
    assert b2.value == 20
    # Equality should compare underlying values
    assert b2 == Box(20)
    assert b1 != b2

def test_box_bind_returns_mapped_value():
    b = Box("hello")
    # bind should apply the function and return its result directly
    result = b.bind(lambda s: s.upper())
    assert result == "HELLO"
    # bind should not wrap the result back into a Box
    assert not isinstance(result, Box)

def test_box_conversion_to_other_monads(tmp_path):
    # Create a Box with a path string
    path_str = str(tmp_path / "file.txt")
    b = Box(path_str)
    # Convert to Maybe, Either, Lazy, Try, and Validation
    maybe = b.to_maybe()
    either = b.to_either()
    lazy = b.to_lazy()
    try_monad = b.to_try()
    validation = b.to_validation()
    # All conversions should preserve the original value
    assert maybe.is_just() and maybe.value == path_str
    assert either.is_right() and either.value == path_str
    assert lazy.is_lazy() and lazy.value() == path_str
    assert try_monad.is_success() and try_monad.value == path_str
    assert validation.is_success() and validation.value == path_str
