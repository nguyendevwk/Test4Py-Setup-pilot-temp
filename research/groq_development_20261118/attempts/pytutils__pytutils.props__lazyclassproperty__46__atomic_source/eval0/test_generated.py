import pytest
from pytutils.props import lazyclassproperty

# Assume classproperty is available in the same module
from pytutils.props import classproperty


class Counter:
    """Helper to count how many times the function is called."""
    def __init__(self):
        self.calls = 0

    def inc(self, cls):
        self.calls += 1
        return self.calls


def test_lazyclassproperty_caches_value():
    """The property should compute the value only once per class."""
    counter = Counter()

    class MyClass:
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    # First access triggers computation
    assert MyClass.value == 1
    # Subsequent accesses return cached value
    assert MyClass.value == 1
    assert MyClass.value == 1
    # Counter should have been incremented only once
    assert counter.calls == 1


def test_lazyclassproperty_subclass_isolated():
    """Each subclass should have its own cached value."""
    counter = Counter()

    class Base:
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    class Sub(Base):
        pass

    # Access on Base
    assert Base.value == 1
    # Access on Sub triggers separate computation
    assert Sub.value == 1
    # Counter should have been incremented twice (once per class)
    assert counter.calls == 2
    # Re-access to ensure caching per subclass
    assert Base.value == 1
    assert Sub.value == 1
    assert counter.calls == 2


def test_lazyclassproperty_raises_exception():
    """If the underlying function raises, the exception propagates."""
    class MyClass:
        @lazyclassproperty
        def value(cls):
            raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        _ = MyClass.value
    # Subsequent access should still raise the same exception
    with pytest.raises(ValueError, match="boom"):
        _ = MyClass.value
