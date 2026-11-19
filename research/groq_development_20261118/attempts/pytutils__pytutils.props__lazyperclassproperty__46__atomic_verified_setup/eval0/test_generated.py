import pytest
from pytutils.props import lazyperclassproperty

# Helper class to track calls
class Counter:
    def __init__(self):
        self.calls = 0

    def __call__(self, cls):
        self.calls += 1
        return f"computed_{cls.__name__}"

def test_lazyperclassproperty_computes_once_per_class():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    # First access triggers computation
    assert Base.value == "computed_Base"
    assert counter.calls == 1

    # Subsequent access uses cached value
    assert Base.value == "computed_Base"
    assert counter.calls == 1

def test_lazyperclassproperty_is_isolated_per_subclass():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    class Sub(Base):
        pass

    # Base and Sub compute separately
    assert Base.value == "computed_Base"
    assert Sub.value == "computed_Sub"
    assert counter.calls == 2

    # Re-access to confirm caching
    assert Base.value == "computed_Base"
    assert Sub.value == "computed_Sub"
    assert counter.calls == 2

def test_lazyperclassproperty_attribute_name_is_unique_and_accessible():
    counter = Counter()

    class Base:
        @lazyperclassproperty
        def value(cls):
            return counter(cls)

    # The attribute name should be stored on the class
    attr_name = f"_Base_lazy_value"
    assert hasattr(Base, attr_name)
    assert getattr(Base, attr_name) == "computed_Base"

    # Ensure that accessing via the property uses the same attribute
    assert Base.value == getattr(Base, attr_name)
    assert counter.calls == 1
