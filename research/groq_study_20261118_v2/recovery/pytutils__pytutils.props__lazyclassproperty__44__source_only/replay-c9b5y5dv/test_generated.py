import pytest
from pytutils.props import lazyclassproperty, classproperty

class Base:
    counter = 0

    @lazyclassproperty
    def value(cls):
        cls.counter += 1
        return cls.counter

class Sub(Base):
    pass

def test_lazyclassproperty_evaluates_once():
    # First access triggers evaluation
    assert Base.value == 1
    # Subsequent access returns cached value
    assert Base.value == 1
    # Counter should have incremented only once
    assert Base.counter == 1

def test_lazyclassproperty_inheritance():
    # Subclass inherits the property but uses its own cache
    assert Sub.value == 1
    # Base counter unchanged
    assert Base.counter == 1
    # Access again on subclass, still cached
    assert Sub.value == 1
    assert Sub.counter == 1

def test_lazyclassproperty_cache_is_class_specific():
    # Reset counters
    Base.counter = 0
    Sub.counter = 0
    # Access Base first
    assert Base.value == 1
    # Access Sub, should compute separately
    assert Sub.value == 1
    # Counters should be independent
    assert Base.counter == 1
    assert Sub.counter == 1

def test_lazyclassproperty_error_propagation():
    class ErrorClass:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad property")

    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorClass.bad
    # After error, accessing again should raise again, not cache
    with pytest.raises(ValueError, match="bad property"):
        _ = ErrorClass.bad
