import pytest
from pytutils.props import lazyclassproperty


class Base:
    counter = 0

    @lazyclassproperty
    def value(cls):
        cls.counter += 1
        return cls.counter


class Derived(Base):
    pass


def test_lazyclassproperty_caches_value(tmp_path):
    """The property should compute once and cache the result."""
    # First access triggers computation
    first = Base.value
    assert first == 1
    # Subsequent access returns cached value
    second = Base.value
    assert second == 1
    # Counter should have incremented only once
    assert Base.counter == 1


def test_lazyclassproperty_inheritance(tmp_path):
    """Derived classes should have separate cached values."""
    # Base computes its own value
    assert Base.value == 1
    # Derived computes its own value independently
    assert Derived.value == 1
    # Counter increments twice, once per class
    assert Base.counter == 2
    assert Derived.counter == 1


def test_lazyclassproperty_error_propagation(tmp_path):
    """If the underlying function raises, the exception propagates."""
    class ErrorClass:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad property")

    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorClass.bad
