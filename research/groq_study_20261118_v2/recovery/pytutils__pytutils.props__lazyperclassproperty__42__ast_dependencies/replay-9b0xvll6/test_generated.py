import pytest
from pytutils.props import lazyperclassproperty, roclassproperty

# Helper to count calls
class Counter:
    def __init__(self):
        self.calls = 0

    def __call__(self, cls):
        self.calls += 1
        return f"computed_for_{cls.__name__}"


def test_lazyperclassproperty_caches_per_class():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    # First access on Base should compute
    assert Base.value == "computed_for_Base"
    assert counter.calls == 1

    # Subsequent access on Base should use cache
    assert Base.value == "computed_for_Base"
    assert counter.calls == 1

    # Subclass should compute separately
    class Sub(Base):
        pass

    assert Sub.value == "computed_for_Sub"
    assert counter.calls == 2

    # Subclass again should use its own cache
    assert Sub.value == "computed_for_Sub"
    assert counter.calls == 2

    # Base still uses its cache
    assert Base.value == "computed_for_Base"
    assert counter.calls == 2


def test_lazyperclassproperty_access_via_instance():
    counter = Counter()

    class MyClass:
        @lazyperclassproperty
        def data(cls):
            return counter(cls)

    instance = MyClass()
    # Access via instance should delegate to class property
    assert instance.data == "computed_for_MyClass"
    assert counter.calls == 1

    # Subsequent instance access uses cache
    assert instance.data == "computed_for_MyClass"
    assert counter.calls == 1


def test_lazyperclassproperty_error_propagation():
    def faulty(cls):
        raise ValueError("bad")

    class Faulty:
        @lazyperclassproperty
        def bad(cls):
            return faulty(cls)

    with pytest.raises(ValueError, match="bad"):
        _ = Faulty.bad

    # After error, subsequent access should raise again (no caching)
    with pytest.raises(ValueError, match="bad"):
        _ = Faulty.bad


def test_lazyperclassproperty_with_roclassproperty():
    # Ensure that lazyperclassproperty works with roclassproperty internally
    counter = Counter()

    class Test:
        @lazyperclassproperty
        def prop(cls):
            return counter(cls)

    # roclassproperty is used internally; accessing via class should work
    assert Test.prop == "computed_for_Test"
    assert counter.calls == 1

    # Access via instance
    t = Test()
    assert t.prop == "computed_for_Test"
    assert counter.calls == 1
