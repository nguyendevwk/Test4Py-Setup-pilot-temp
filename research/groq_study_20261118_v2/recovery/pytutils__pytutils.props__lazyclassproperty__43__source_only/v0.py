import pytest
from pytutils.props import lazyclassproperty

# Helper class to capture calls
class Counter:
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

def test_lazyclassproperty_inheritance():
    counter = Counter()

    class Base:
        @lazyclassproperty
        def val(cls):
            return counter.inc(cls)

    class Child(Base):
        pass

    # Base class computes once
    assert Base.val == 1
    assert counter.calls == 1

    # Child class computes separately
    assert Child.val == 1
    assert counter.calls == 2

    # Re-accessing child does not recompute
    assert Child.val == 1
    assert counter.calls == 2

def test_lazyclassproperty_attribute_name():
    counter = Counter()

    class Test:
        @lazyclassproperty
        def prop(cls):
            return counter.inc(cls)

    # Attribute name should be prefixed with _lazy_
    assert hasattr(Test, "_lazy_prop")
    assert Test._lazy_prop == 1

def test_lazyclassproperty_error_propagation():
    class Test:
        @lazyclassproperty
        def bad(cls):
            raise ValueError("bad")

    with pytest.raises(ValueError, match="bad"):
        _ = Test.bad

    # After error, attribute should not be set
    assert not hasattr(Test, "_lazy_bad")

def test_lazyclassproperty_is_classproperty():
    class Test:
        @lazyclassproperty
        def prop(cls):
            return 42

    # The descriptor should be a classproperty instance
    from pytutils.props import classproperty
    assert isinstance(Test.__dict__["prop"], classproperty)

def test_lazyclassproperty_with_subclass_overrides():
    counter = Counter()

    class Base:
        @lazyclassproperty
        def val(cls):
            return counter.inc(cls)

    class Child(Base):
        @lazyclassproperty
        def val(cls):
            return counter.inc(cls) + 100

    # Base and Child compute independently
    assert Base.val == 1
    assert Child.val == 101
    assert counter.calls == 2

    # Re-accessing does not recompute
    assert Base.val == 1
    assert Child.val == 101
    assert counter.calls == 2
