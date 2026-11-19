# Module: genty.genty_repeat
import pytest
from genty.genty_repeat import genty_repeat

def test_genty_repeat_positive_count():
    def test_method():
        pass

    wrapped_method = genty_repeat(5)(test_method)
    assert hasattr(wrapped_method, 'genty_repeat_count')
    assert wrapped_method.genty_repeat_count == 5

def test_genty_repeat_zero_count():
    def test_method():
        pass

    wrapped_method = genty_repeat(0)(test_method)
    assert hasattr(wrapped_method, 'genty_repeat_count')
    assert wrapped_method.genty_repeat_count == 0

def test_genty_repeat_negative_count():
    with pytest.raises(ValueError):
        @genty_repeat(-1)
        def test_method():
            pass

def test_genty_repeat_large_count():
    def test_method():
        pass

    wrapped_method = genty_repeat(1000)(test_method)
    assert hasattr(wrapped_method, 'genty_repeat_count')
    assert wrapped_method.genty_repeat_count == 1000

def test_genty_repeat_with_decorator_chaining():
    def test_method(bool_value):
        pass

    wrapped_method = genty_repeat(3)(test_method)
    assert hasattr(wrapped_method, 'genty_repeat_count')
    assert wrapped_method.genty_repeat_count == 3
