import pytest
from pytutils.props import lazyclassproperty, roclassproperty

# Helper class to track calls
class Counter:
    def __init__(self):
        self.calls = 0

    def inc(self, cls):
        self.calls += 1
        return self.calls

# Test that the property is evaluated lazily and cached
def test_lazyclassproperty_evaluates_once():
    counter = Counter()

    class Test:
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    # First access triggers evaluation
    assert Test.value == 1
    # Subsequent accesses return cached value
    assert Test.value == 1
    # Counter should have been called only once
    assert counter.calls == 1

# Test that the property is shared across subclasses
def test_lazyclassproperty_subclass_shared():
    counter = Counter()

    class Base:
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    class Sub(Base):
        pass

    # Access on Base
    assert Base.value == 1
    # Access on Sub, should return the same cached value
    assert Sub.value == 1
    # Counter called only once, shared between Base and Sub
    assert counter.calls == 1

# Test that an exception in the factory propagates
def test_lazyclassproperty_exception_propagation():
    class Test:
        @lazyclassproperty
        def value(cls):
            raise RuntimeError("factory error")

    with pytest.raises(RuntimeError, match="factory error"):
        _ = Test.value

# Test that the descriptor works with classproperty directly
def test_classproperty_direct():
    class Test:
        @roclassproperty
        def value(cls):
            return 123

    assert Test.value == 123
    # Setting the attribute creates a new class attribute, overriding the descriptor
    Test.value = 456
    assert Test.value == 456
