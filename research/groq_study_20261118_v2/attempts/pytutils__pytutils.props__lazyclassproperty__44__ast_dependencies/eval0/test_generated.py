import pytest
from pytutils.props import lazyclassproperty, roclassproperty


class Counter:
    """Helper class to count how many times a function is called."""
    def __init__(self):
        self.calls = 0

    def inc(self, cls):
        self.calls += 1
        return self.calls


def test_lazyclassproperty_caches_value():
    counter = Counter()

    class Test:
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    # First access triggers computation
    assert Test.value == 1
    assert counter.calls == 1

    # Subsequent accesses return cached value
    assert Test.value == 1
    assert counter.calls == 1

    # Access from subclass inherits cached value but recomputes for subclass
    class Sub(Test):
        pass

    assert Sub.value == 1
    assert counter.calls == 1  # still 1 because Sub inherits cached value

    # If subclass overrides the property, it recomputes
    class SubOverride(Test):
        @lazyclassproperty
        def value(cls):
            return counter.inc(cls)

    assert SubOverride.value == 2
    assert counter.calls == 2
    assert SubOverride.value == 2
    assert counter.calls == 2


def test_lazyclassproperty_with_error():
    class TestError:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad property")

    with pytest.raises(ValueError, match="bad property"):
        _ = TestError.bad

    # After error, attribute should not be cached; next access still raises
    with pytest.raises(ValueError, match="bad property"):
        _ = TestError.bad


def test_lazyclassproperty_is_readonly():
    class TestReadOnly:
        @lazyclassproperty
        def data(cls):
            return [1, 2, 3]

    # Access property
    assert TestReadOnly.data == [1, 2, 3]

    # Attempt to set attribute should raise AttributeError
    with pytest.raises(AttributeError):
        TestReadOnly.data = [4, 5, 6]


def test_lazyclassproperty_with_classproperty_decorator():
    # Ensure that lazyclassproperty uses the underlying roclassproperty correctly
    class TestRO:
        @roclassproperty
        def ro(cls):
            return "ro"

    class TestLazy:
        @lazyclassproperty
        def ro(cls):
            return "lazy"

    assert TestRO.ro == "ro"
    assert TestLazy.ro == "lazy"


def test_lazyclassproperty_multiple_instances():
    counter = Counter()

    class TestMulti:
        @lazyclassproperty
        def val(cls):
            return counter.inc(cls)

    # Multiple accesses across different classes
    class A(TestMulti):
        pass

    class B(TestMulti):
        pass

    assert A.val == 1
    assert B.val == 1
    assert counter.calls == 1  # both share same cached value

    # After accessing B, value remains same
    assert B.val == 1
    assert counter.calls == 1

    # If we delete the cached attribute from A, B still has it
    delattr(A, "_lazy_val")
    assert A.val == 1
    assert counter.calls == 1
