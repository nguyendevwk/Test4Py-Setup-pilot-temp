import pytest
from pytutils.props import lazyperclassproperty

# Helper class to track function calls
class Counter:
    def __init__(self):
        self.calls = 0

    def __call__(self, cls):
        self.calls += 1
        return f"computed for {cls.__name__}"

def test_lazyperclassproperty_caches_value_per_class():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    # First access triggers computation
    assert Base.value == "computed for Base"
    assert counter.calls == 1

    # Subsequent access uses cached value
    assert Base.value == "computed for Base"
    assert counter.calls == 1

def test_lazyperclassproperty_separate_cache_for_subclass():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    class Sub(Base):
        pass

    # Access on Base and Sub should compute separately
    assert Base.value == "computed for Base"
    assert Sub.value == "computed for Sub"
    assert counter.calls == 2

    # Re-access to confirm caching
    assert Base.value == "computed for Base"
    assert Sub.value == "computed for Sub"
    assert counter.calls == 2

def test_lazyperclassproperty_raises_exception_and_does_not_cache():
    class Base:
        @lazyperclassproperty
        def value(cls):
            raise RuntimeError("computation failed")

    with pytest.raises(RuntimeError, match="computation failed"):
        _ = Base.value

    # After exception, accessing again should raise again (no caching)
    with pytest.raises(RuntimeError, match="computation failed"):
        _ = Base.value
